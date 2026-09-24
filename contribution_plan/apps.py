from django.apps import AppConfig

from core.rights_declaration import RightsDeclaration

MODULE_NAME = "contribution_plan"


# Rights, by entity then by action.
#
# The module carries three distinct business entities, each with its own block of
# identifiers: contributionPlanBundle (1511xx), contributionPlan (1512xx) and
# paymentPlan (1571xx). These really are three separate objects - a bundle groups
# contribution plans, a payment plan is an object apart - and not three views of one
# object: no identifier is shared between them.
#
# `replace` is a business action and not an `update`: replacing creates a new version of
# the object and closes the old one (`replacement_uuid`), where `update` modifies the
# object in place. openIMIS gave it its own identifier (the 06 of each block), and we do
# not force it into the canonical verb.
#
# `queryAdmins` (the 05 of each block) is a dormant declaration: see the comment on the
# matching attributes in ContributionPlanConfig.
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


# Empty: the module has no setting outside the rights, and the rights no longer go
# through the configuration. `ready()` is kept so that a future setting has somewhere to
# land.
DEFAULT_CFG = {}


class ContributionPlanConfig(AppConfig):
    name = MODULE_NAME

    # Rights: constants derived from DJANGO_PERMS, no longer overridable. They go
    # neither through DEFAULT_CFG nor through ready():
    # `ModuleConfiguration.get_or_default` now ignores any `_perms` key stored in the
    # database.
    gql_query_contributionplanbundle_perms = RIGHTS.perms("contributionPlanBundle", "query")
    # A dormant declaration: no resolver and no mutation reads this key (neither here
    # nor in another module). We keep it because identifier 151105 is already granted to
    # deployed roles, and we leave it its declared value rather than [] -
    # `has_perms([])` returns True, so an empty list would grant everybody the action
    # this key will eventually guard.
    gql_query_contributionplanbundle_admins_perms = RIGHTS.perms("contributionPlanBundle", "queryAdmins")

    gql_query_contributionplan_perms = RIGHTS.perms("contributionPlan", "query")
    # A dormant declaration, same reason as above (identifier 151205).
    gql_query_contributionplan_admins_perms = RIGHTS.perms("contributionPlan", "queryAdmins")

    gql_query_paymentplan_perms = RIGHTS.perms("paymentPlan", "query")
    # A dormant declaration, same reason as above (identifier 157105).
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
