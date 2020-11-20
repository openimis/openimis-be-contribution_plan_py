import graphene
from core.schema import OpenIMISMutation, TinyInt


class ContributionPlanBundleInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)
    version = graphene.Int(required=True)

    active = graphene.Boolean()
    code = graphene.String(max_length=255)
    name = graphene.String(max_length=255)

    json_ext = graphene.types.json.JSONString(required=False)

    date_created = graphene.DateTime(required=False)
    date_updated = graphene.DateTime(required=False)

    user_updated = graphene.Int(required=False)
    user_created = graphene.Int(required=False)

    date_valid_from = graphene.DateTime(required=False)
    date_valid_to = graphene.DateTime(required=False)


class ContributionPlanInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)
    version = graphene.Int(required=True)

    active = graphene.Boolean()
    code = graphene.String(max_length=255)
    benefit_plan_id = graphene.Int(required=False)
    periodicity = graphene.Int(required=False)

    json_ext = graphene.types.json.JSONString(required=False)

    amendment = graphene.Int(required=False)

    date_created = graphene.DateTime(required=False)
    date_updated = graphene.DateTime(required=False)

    user_updated = graphene.Int(required=False)
    user_created = graphene.Int(required=False)

    date_valid_from = graphene.DateTime(required=False)
    date_valid_to = graphene.DateTime(required=False)


class ContributionPlanBundleDetailsInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)
    version = graphene.Int(required=True)

    contribution_plan_bundle_id = graphene.Int(required=True)
    contribution_plan_id = graphene.Int(required=True)

    json_ext = graphene.types.json.JSONString(required=False)

    date_created = graphene.DateTime(required=False)
    date_updated = graphene.DateTime(required=False)

    user_updated = graphene.Int(required=False)
    user_created = graphene.Int(required=False)

    date_valid_from = graphene.DateTime(required=False)
    date_valid_to = graphene.DateTime(required=False)

    active = graphene.Boolean()
