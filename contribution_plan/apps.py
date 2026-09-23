from django.apps import AppConfig

from core.rights_declaration import RightsDeclaration

MODULE_NAME = "contribution_plan"


# Droits, par entite puis par action.
#
# Le module porte trois entites metier distinctes, chacune avec son propre bloc
# d'identifiants : contributionPlanBundle (1511xx), contributionPlan (1512xx) et
# paymentPlan (1571xx). Ce sont bien trois objets separes - un bundle regroupe des
# plans de contribution, un payment plan est un objet a part - et non trois vues d'un
# meme objet : aucun identifiant n'est partage entre eux.
#
# `replace` est une action metier et non un `update` : remplacer cree une nouvelle
# version de l'objet et cloture l'ancienne (`replacement_uuid`), la ou `update` modifie
# l'objet en place. openIMIS lui a donne son propre identifiant (le 06 de chaque bloc),
# on ne le force pas dans le verbe canonique.
#
# `queryAdmins` (le 05 de chaque bloc) est une declaration dormante : voir le
# commentaire sur les attributs correspondants dans ContributionPlanConfig.
DJANGO_PERMS = {
    "contributionPlanBundle": {
        "query": ("contribution_plan.view_contributionplanbundle", 151101),
        "create": ("contribution_plan.add_contributionplanbundle", 151102),
        "update": ("contribution_plan.change_contributionplanbundle", 151103),
        "delete": ("contribution_plan.delete_contributionplanbundle", 151104),
        "queryAdmins": ("contribution_plan.view_contributionplanbundle_admin", 151105),
        "replace": ("contribution_plan.replace_contributionplanbundle", 151106),
    },
    "contributionPlan": {
        "query": ("contribution_plan.view_contributionplan", 151201),
        "create": ("contribution_plan.add_contributionplan", 151202),
        "update": ("contribution_plan.change_contributionplan", 151203),
        "delete": ("contribution_plan.delete_contributionplan", 151204),
        "queryAdmins": ("contribution_plan.view_contributionplan_admin", 151205),
        "replace": ("contribution_plan.replace_contributionplan", 151206),
    },
    "paymentPlan": {
        "query": ("contribution_plan.view_paymentplan", 157101),
        "create": ("contribution_plan.add_paymentplan", 157102),
        "update": ("contribution_plan.change_paymentplan", 157103),
        "delete": ("contribution_plan.delete_paymentplan", 157104),
        "queryAdmins": ("contribution_plan.view_paymentplan_admin", 157105),
        "replace": ("contribution_plan.replace_paymentplan", 157106),
    },
}

_PERM_CFG = {
    "gql_query_contributionplanbundle_perms": ("contributionPlanBundle", "query"),
    "gql_query_contributionplanbundle_admins_perms": ("contributionPlanBundle", "queryAdmins"),
    "gql_mutation_create_contributionplanbundle_perms": ("contributionPlanBundle", "create"),
    "gql_mutation_update_contributionplanbundle_perms": ("contributionPlanBundle", "update"),
    "gql_mutation_delete_contributionplanbundle_perms": ("contributionPlanBundle", "delete"),
    "gql_mutation_replace_contributionplanbundle_perms": ("contributionPlanBundle", "replace"),
    "gql_query_contributionplan_perms": ("contributionPlan", "query"),
    "gql_query_contributionplan_admins_perms": ("contributionPlan", "queryAdmins"),
    "gql_mutation_create_contributionplan_perms": ("contributionPlan", "create"),
    "gql_mutation_update_contributionplan_perms": ("contributionPlan", "update"),
    "gql_mutation_delete_contributionplan_perms": ("contributionPlan", "delete"),
    "gql_mutation_replace_contributionplan_perms": ("contributionPlan", "replace"),
    "gql_query_paymentplan_perms": ("paymentPlan", "query"),
    "gql_query_paymentplan_admins_perms": ("paymentPlan", "queryAdmins"),
    "gql_mutation_create_paymentplan_perms": ("paymentPlan", "create"),
    "gql_mutation_update_paymentplan_perms": ("paymentPlan", "update"),
    "gql_mutation_delete_paymentplan_perms": ("paymentPlan", "delete"),
    "gql_mutation_replace_paymentplan_perms": ("paymentPlan", "replace"),
}

RIGHTS = RightsDeclaration(MODULE_NAME, DJANGO_PERMS, _PERM_CFG)

perms = RIGHTS.perms
django_perms = RIGHTS.django_perm_names
configured_perms = RIGHTS.configured
require = RIGHTS.require


# Vide : le module n'a aucun reglage hors droits, et les droits ne passent plus par la
# configuration. `ready()` est conserve pour qu'un reglage futur ait ou atterrir.
DEFAULT_CFG = {}


class ContributionPlanConfig(AppConfig):
    name = MODULE_NAME

    # Droits: constantes issues de DJANGO_PERMS, plus surchargeables. Ils ne
    # passent plus par le DEFAULT_CFG ni par ready(): `ModuleConfiguration.get_or_default`
    # ignore desormais toute cle `_perms` stockee en base.
    gql_query_contributionplanbundle_perms = RIGHTS.perms("contributionPlanBundle", "query")
    # Declaration dormante : aucun resolver ni mutation ne lit cette cle (ni ici, ni
    # dans un autre module). On la conserve parce que l'identifiant 151105 est deja
    # accorde a des roles deployes, et on lui laisse sa valeur declaree plutot que []
    # - `has_perms([])` renvoie True, donc une liste vide accorderait a tout le monde
    # l'action que cette cle finira par garder.
    gql_query_contributionplanbundle_admins_perms = RIGHTS.perms("contributionPlanBundle", "queryAdmins")

    gql_query_contributionplan_perms = RIGHTS.perms("contributionPlan", "query")
    # Declaration dormante, meme raison que ci-dessus (identifiant 151205).
    gql_query_contributionplan_admins_perms = RIGHTS.perms("contributionPlan", "queryAdmins")

    gql_query_paymentplan_perms = RIGHTS.perms("paymentPlan", "query")
    # Declaration dormante, meme raison que ci-dessus (identifiant 157105).
    gql_query_paymentplan_admins_perms = RIGHTS.perms("paymentPlan", "queryAdmins")

    gql_mutation_create_contributionplanbundle_perms = RIGHTS.perms("contributionPlanBundle", "create")
    gql_mutation_update_contributionplanbundle_perms = RIGHTS.perms("contributionPlanBundle", "update")
    gql_mutation_delete_contributionplanbundle_perms = RIGHTS.perms("contributionPlanBundle", "delete")
    gql_mutation_replace_contributionplanbundle_perms = RIGHTS.perms("contributionPlanBundle", "replace")

    gql_mutation_create_contributionplan_perms = RIGHTS.perms("contributionPlan", "create")
    gql_mutation_update_contributionplan_perms = RIGHTS.perms("contributionPlan", "update")
    gql_mutation_delete_contributionplan_perms = RIGHTS.perms("contributionPlan", "delete")
    gql_mutation_replace_contributionplan_perms = RIGHTS.perms("contributionPlan", "replace")

    gql_mutation_create_paymentplan_perms = RIGHTS.perms("paymentPlan", "create")
    gql_mutation_update_paymentplan_perms = RIGHTS.perms("paymentPlan", "update")
    gql_mutation_delete_paymentplan_perms = RIGHTS.perms("paymentPlan", "delete")
    gql_mutation_replace_paymentplan_perms = RIGHTS.perms("paymentPlan", "replace")

    def __load_config(self, cfg):
        for field in cfg:
            if hasattr(ContributionPlanConfig, field):
                setattr(ContributionPlanConfig, field, cfg[field])

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self.__load_config(cfg)
