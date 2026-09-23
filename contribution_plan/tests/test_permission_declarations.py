"""
Guard rails on contribution_plan's rights declaration.

Same structure as `claim` and `product`: `DJANGO_PERMS` by entity then by action,
`_PERM_CFG` deriving the config keys from it, and a `get_rights` on each main model
which is only an access point.

What is locked down here is the entity/action pair, not only the values:
  * an identifier in one place only (DJANGO_PERMS), hence no drift between the
    DEFAULT_CFG and the check;
  * a config key with no class attribute is never loaded by `__load_config` and
    reading it raises AttributeError - the right becomes unenforceable;
  * `has_perms([])` returns True, so an empty list grants to everybody.

The module carries three separate entities (1511xx / 1512xx / 1571xx): no identifier is
shared, and the test below verifies it.
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

# The identifiers as deployed. Changing one is incompatible with the existing roles:
# this test has to be updated *and* the new right granted.
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

# The `permissions_map.json` entries that carry these identifiers. The historical name
# in the openIMIS catalogue is not the django name declared in DJANGO_PERMS: what has to
# stay stable is the integer.
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

# Keys declared but which no call site reads. Kept because the identifiers are already
# granted to deployed roles; listed here so that adding a reader, or removing the key,
# is a visible decision.
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
    """`permissions_map.json` lives in the assembly, not in the package."""
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
        """`__load_config` ignores the keys with no class attribute."""
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
        """Three distinct business objects, three disjoint blocks of identifiers."""
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
        Nobody reads them; they must carry their identifier all the same, and not [],
        otherwise the day a check does read them it will grant the action to everybody.
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

    # --- the access point through the model -------------------------------
    def test_each_model_exposes_every_action_of_its_entity(self):
        for entity, model in MODEL_BY_ENTITY.items():
            for action in DJANGO_PERMS[entity]:
                with self.subTest(entity=entity, action=action):
                    self.assertEqual(
                        model.get_rights(action), configured_perms(entity, action)
                    )
                    self.assertTrue(model.get_rights(action))

    def test_model_returns_none_for_an_undeclared_action(self):
        """None means "no rule": the caller must fail closed."""
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

    # --- the sub-resource --------------------------------------------------
    def test_bundle_details_delegates_to_the_bundle(self):
        """
        Two FKs, a single owner: composing a bundle takes the bundle's right, not that
        of the contribution plan it references.
        """
        from core.rights_scope import scope_parent_of

        self.assertEqual(
            ContributionPlanBundleDetails.scope_parent, "contribution_plan_bundle"
        )
        self.assertIs(
            scope_parent_of(ContributionPlanBundleDetails), ContributionPlanBundle
        )
        self.assertFalse(hasattr(ContributionPlanBundleDetails, "get_rights"))
