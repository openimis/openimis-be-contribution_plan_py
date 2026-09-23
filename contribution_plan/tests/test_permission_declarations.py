"""
Garde-fous sur la declaration des droits de contribution_plan.

Meme structure que `claim` et `product` : `DJANGO_PERMS` par entite puis par action,
`_PERM_CFG` qui en derive les cles de config, et un `get_rights` sur chaque modele
principal qui n'est qu'un point d'acces.

Ce qui est verrouille ici, c'est le couple entite/action, pas seulement les valeurs :
  * un identifiant a un seul endroit (DJANGO_PERMS), donc pas de derive entre le
    DEFAULT_CFG et le controle ;
  * une cle de config sans attribut de classe n'est jamais chargee par `__load_config`
    et sa lecture leve AttributeError - le droit devient inapplicable ;
  * `has_perms([])` renvoie True, donc une liste vide accorde a tous.

Le module porte trois entites separees (1511xx / 1512xx / 1571xx) : aucun identifiant
n'est partage, et le test ci-dessous le verifie.
"""

import json
import os

from django.test import TestCase

from contribution_plan.apps import (
    DJANGO_PERMS,
    ContributionPlanConfig,
    _PERM_CFG,
    configured_perms,
    django_perms,
    perms,
)
from contribution_plan.models import (
    ContributionPlan,
    ContributionPlanBundle,
    ContributionPlanBundleDetails,
    PaymentPlan,
)

# Les identifiants tels que deployes. En changer un est incompatible avec les roles
# existants : il faut mettre ce test a jour *et* accorder le nouveau droit.
EXPECTED_RIGHTS = {
    "gql_query_contributionplanbundle_perms": ["151101"],
    "gql_query_contributionplanbundle_admins_perms": ["151105"],
    "gql_mutation_create_contributionplanbundle_perms": ["151102"],
    "gql_mutation_update_contributionplanbundle_perms": ["151103"],
    "gql_mutation_delete_contributionplanbundle_perms": ["151104"],
    "gql_mutation_replace_contributionplanbundle_perms": ["151106"],
    "gql_query_contributionplan_perms": ["151201"],
    "gql_query_contributionplan_admins_perms": ["151205"],
    "gql_mutation_create_contributionplan_perms": ["151202"],
    "gql_mutation_update_contributionplan_perms": ["151203"],
    "gql_mutation_delete_contributionplan_perms": ["151204"],
    "gql_mutation_replace_contributionplan_perms": ["151206"],
    "gql_query_paymentplan_perms": ["157101"],
    "gql_query_paymentplan_admins_perms": ["157105"],
    "gql_mutation_create_paymentplan_perms": ["157102"],
    "gql_mutation_update_paymentplan_perms": ["157103"],
    "gql_mutation_delete_paymentplan_perms": ["157104"],
    "gql_mutation_replace_paymentplan_perms": ["157106"],
}

# Les entrees de `permissions_map.json` qui portent ces identifiants. Le nom historique
# du catalogue openIMIS n'est pas le nom django declare dans DJANGO_PERMS : ce qui doit
# rester stable, c'est l'entier.
EXPECTED_MAP_ENTRIES = {
    "contribution_plan.contributionplanbundle": "151101",
    "contribution_plan.create_contributionplanbundle": "151102",
    "contribution_plan.update_contributionplanbundle": "151103",
    "contribution_plan.delete_contributionplanbundle": "151104",
    "contribution_plan.contributionplanbundle_admins": "151105",
    "contribution_plan.replace_contributionplanbundle": "151106",
    "contribution_plan.contributionplan": "151201",
    "contribution_plan.create_contributionplan": "151202",
    "contribution_plan.update_contributionplan": "151203",
    "contribution_plan.delete_contributionplan": "151204",
    "contribution_plan.contributionplan_admins": "151205",
    "contribution_plan.replace_contributionplan": "151206",
    "contribution_plan.paymentplan": "157101",
    "contribution_plan.create_paymentplan": "157102",
    "contribution_plan.update_paymentplan": "157103",
    "contribution_plan.delete_paymentplan": "157104",
    "contribution_plan.paymentplan_admins": "157105",
    "contribution_plan.replace_paymentplan": "157106",
}

# Cles declarees mais qu'aucun site d'appel ne lit. Conservees parce que les
# identifiants sont deja accordes a des roles deployes ; listees ici pour que l'ajout
# d'un lecteur, ou la suppression de la cle, soit une decision visible.
DORMANT_KEYS = {
    "gql_query_contributionplanbundle_admins_perms",
    "gql_query_contributionplan_admins_perms",
    "gql_query_paymentplan_admins_perms",
}

MODEL_BY_ENTITY = {
    "contributionPlanBundle": ContributionPlanBundle,
    "contributionPlan": ContributionPlan,
    "paymentPlan": PaymentPlan,
}


def _permissions_map():
    """`permissions_map.json` vit dans l'assemblage, pas dans le paquet."""
    from django.conf import settings

    candidates = [
        os.path.join(str(settings.BASE_DIR), "permissions_map.json"),
        os.path.join(os.path.dirname(str(settings.BASE_DIR)), "permissions_map.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path) as handle:
                return json.load(handle)
    return None


class ContributionPlanPermissionDeclarationTestCase(TestCase):
    def test_right_ids_unchanged(self):
        self.assertEqual(
            {key: getattr(ContributionPlanConfig, key) for key in EXPECTED_RIGHTS},
            EXPECTED_RIGHTS,
        )

    def test_perm_cfg_covers_every_declared_action(self):
        declared = {
            (entity, action)
            for entity, actions in DJANGO_PERMS.items()
            for action in actions
        }
        self.assertEqual(set(_PERM_CFG.values()), declared)

    def test_perm_cfg_matches_config_attributes(self):
        """`__load_config` ignore les cles sans attribut de classe."""
        missing = [key for key in _PERM_CFG if not hasattr(ContributionPlanConfig, key)]
        self.assertEqual(missing, [])

    def test_no_right_list_is_empty(self):
        empty = [key for key in _PERM_CFG if not getattr(ContributionPlanConfig, key)]
        self.assertEqual(empty, [])

    def test_attributes_carry_the_declared_right(self):
        for key, (entity, action) in _PERM_CFG.items():
            with self.subTest(key=key):
                self.assertEqual(
                    getattr(ContributionPlanConfig, key), perms(entity, action)
                )

    def test_the_three_entities_share_no_right_id(self):
        """Trois objets metier distincts, trois blocs d'identifiants disjoints."""
        seen = {}
        for entity, actions in DJANGO_PERMS.items():
            for action, (_, right_id) in actions.items():
                seen.setdefault(right_id, []).append(f"{entity}.{action}")
        shared = {right: who for right, who in seen.items() if len(who) > 1}
        self.assertEqual(shared, {})

    def test_django_permission_names_are_unique(self):
        seen = {}
        for entity, actions in DJANGO_PERMS.items():
            for action, (name, _) in actions.items():
                seen.setdefault(name, []).append(f"{entity}.{action}")
        shared = {name: who for name, who in seen.items() if len(who) > 1}
        self.assertEqual(shared, {})

    def test_unknown_entity_or_action_raises(self):
        with self.assertRaises(KeyError):
            perms("nosuchentity", "query")
        with self.assertRaises(KeyError):
            perms("contributionPlan", "nosuchaction")
        with self.assertRaises(KeyError):
            django_perms("paymentPlan", "nosuchaction")

    def test_dormant_keys_are_still_declared(self):
        """
        Personne ne les lit ; elles doivent malgre tout porter leur identifiant, et non
        [], sinon le jour ou un controle les lira il accordera l'action a tous.
        """
        for key in DORMANT_KEYS:
            with self.subTest(key=key):
                self.assertIn(key, _PERM_CFG)
                self.assertEqual(getattr(ContributionPlanConfig, key), EXPECTED_RIGHTS[key])

    def test_ids_match_permissions_map(self):
        mapping = _permissions_map()
        if mapping is None:
            self.skipTest("permissions_map.json absent de cet assemblage")
        actual = {name: mapping.get(name) for name in EXPECTED_MAP_ENTRIES}
        self.assertEqual(actual, EXPECTED_MAP_ENTRIES)

    # --- le point d'acces par le modele -----------------------------------
    def test_each_model_exposes_every_action_of_its_entity(self):
        for entity, model in MODEL_BY_ENTITY.items():
            for action in DJANGO_PERMS[entity]:
                with self.subTest(entity=entity, action=action):
                    self.assertEqual(
                        model.get_rights(action), configured_perms(entity, action)
                    )
                    self.assertTrue(model.get_rights(action))

    def test_model_returns_none_for_an_undeclared_action(self):
        """None signifie "aucune regle" : l'appelant doit echouer ferme."""
        for model in MODEL_BY_ENTITY.values():
            with self.subTest(model=model.__name__):
                self.assertIsNone(model.get_rights("nosuchaction"))

    def test_model_reads_the_configured_value_not_the_declared_default(self):
        original = ContributionPlanConfig.gql_query_paymentplan_perms
        try:
            ContributionPlanConfig.gql_query_paymentplan_perms = ["999999"]
            self.assertEqual(PaymentPlan.get_rights("query"), ["999999"])
            self.assertEqual(perms("paymentPlan", "query"), ["157101"])
        finally:
            ContributionPlanConfig.gql_query_paymentplan_perms = original

    # --- la sous-ressource -------------------------------------------------
    def test_bundle_details_delegates_to_the_bundle(self):
        """
        Deux FK, un seul proprietaire : composer un bundle prend le droit du bundle,
        pas celui du plan de contribution qu'il reference.
        """
        from core.rights_scope import scope_parent_of

        self.assertEqual(
            ContributionPlanBundleDetails.scope_parent, "contribution_plan_bundle"
        )
        self.assertIs(
            scope_parent_of(ContributionPlanBundleDetails), ContributionPlanBundle
        )
        self.assertFalse(hasattr(ContributionPlanBundleDetails, "get_rights"))
