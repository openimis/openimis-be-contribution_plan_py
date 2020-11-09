import graphene
import graphene_django_optimizer as gql_optimizer
from contribution_plan.gql import ContributionPlanBundleGQLType, ContributionPlanGQLType, \
    ContributionPlanBundleDetailsGQLType
from contribution_plan.gql.gql_mutations.contribution_plan_bundle_details_mutations import \
    CreateContributionPlanBundleDetailsMutation, UpdateContributionPlanBundleDetailsMutation, \
    DeleteContributionPlanBundleDetailsMutation
from contribution_plan.gql.gql_mutations.contribution_plan_bundle_mutations import CreateContributionPlanBundleMutation, \
    UpdateContributionPlanBundleMutation, DeleteContributionPlanBundleMutation
from contribution_plan.gql.gql_mutations.contribution_plan_mutations import CreateContributionPlanMutation, \
    UpdateContributionPlanMutation, DeleteContributionPlanMutation
from contribution_plan.models import ContributionPlanBundle, ContributionPlan, ContributionPlanBundleDetails
from core.schema import OrderedDjangoFilterConnectionField, signal_mutation_module_validate


class Query(graphene.ObjectType):
    contribution_plan_bundle = OrderedDjangoFilterConnectionField(ContributionPlanBundleGQLType)
    contribution_plan = OrderedDjangoFilterConnectionField(ContributionPlanGQLType)
    contribution_plan_bundle_details = OrderedDjangoFilterConnectionField(ContributionPlanBundleDetailsGQLType)

    def resolve_contribution_plan_bundle(self, info, **kwargs):
        query = ContributionPlanBundle.objects
        return gql_optimizer.query(query.all(), info)

    def resolve_contribution_plan(self, info, **kwargs):
        query = ContributionPlan.objects
        return gql_optimizer.query(query.all(), info)

    def resolve_contribution_plan_bundle_details(self, info, **kwargs):
        query = ContributionPlanBundleDetails.objects
        return gql_optimizer.query(query.all(), info)


class Mutation(graphene.ObjectType):
    create_contribution_plan_bundle = CreateContributionPlanBundleMutation.Field()
    create_contribution_plan = CreateContributionPlanMutation.Field()
    create_contribution_plan_bundle_details = CreateContributionPlanBundleDetailsMutation.Field()
    
    update_contribution_plan_bundle = UpdateContributionPlanBundleMutation.Field()
    update_contribution_plan = UpdateContributionPlanMutation.Field()
    update_contribution_plan_bundle_details = UpdateContributionPlanBundleDetailsMutation.Field()
    
    delete_contribution_plan_bundle = DeleteContributionPlanBundleMutation.Field()
    delete_contribution_plan = DeleteContributionPlanMutation.Field()
    delete_contribution_plan_bundle_details = DeleteContributionPlanBundleDetailsMutation.Field()
    

# def on_mutation_base(gql_key, model, sender, **kwargs):
#     uuids = kwargs['data'].get('uuids', [])
#     uuid_key = "{gql_key}_uuid".format(gql_key=gql_key)
#
#     if not uuids:
#         uuid = kwargs['data'].get(uuid_key, None)
#         uuids = [uuid] if uuid else []
#         if not uuids:
#             return []
#         impacted = model.objects.filter(uuid__in=uuids).all()
#
#         for impacted_obj in impacted:
#             create_kwargs = {
#                 gql_key: impacted_obj,
#                 'mutation_id': kwargs['mutation_log_id']
#             }
#             model.objects.create(**create_kwargs)
#
#
# def on_contribution_plan_bundle_mutation(sender, **kwargs):
#     on_mutation_base('contribution_plan_bundle', ContributionPlanBundle, sender, **kwargs)
#     return []
#
#
# def on_contribution_plan_mutation(sender, **kwargs):
#     on_mutation_base('contribution_plan', ContributionPlan, sender, **kwargs)
#     return []
#
#
# def on_contribution_plan__bundle_details_mutation(sender, **kwargs):
#     on_mutation_base('contribution_plan_bundle_details', ContributionPlanBundleDetails, sender, **kwargs)
#     return []
#
#
# def bind_signals():
#     signal_mutation_module_validate["contribution_plan_bundle"].connect(on_contribution_plan_bundle_mutation)
#     signal_mutation_module_validate["contribution_plan"].connect(on_contribution_plan_mutation)
#     signal_mutation_module_validate["contribution_plan_bundle_details"]\
#         .connect(on_contribution_plan__bundle_details_mutation)

