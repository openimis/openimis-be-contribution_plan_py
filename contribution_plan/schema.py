import graphene
import graphene_django_optimizer as gql_optimizer

from core.schema import signal_mutation_module_validate
from contribution_plan.gql import ContributionPlanGQLType, ContributionPlanBundleGQLType, \
    ContributionPlanBundleDetailsGQLType
from contribution_plan.gql.gql_mutations.contribution_plan_bundle_details_mutations import \
    CreateContributionPlanBundleDetailsMutation, UpdateContributionPlanBundleDetailsMutation, \
    DeleteContributionPlanBundleDetailsMutation, ReplaceContributionPlanBundleDetailsMutation
from contribution_plan.gql.gql_mutations.contribution_plan_bundle_mutations import CreateContributionPlanBundleMutation, \
    UpdateContributionPlanBundleMutation, DeleteContributionPlanBundleMutation, ReplaceContributionPlanBundleMutation
from contribution_plan.gql.gql_mutations.contribution_plan_mutations import CreateContributionPlanMutation, \
    UpdateContributionPlanMutation, DeleteContributionPlanMutation, ReplaceContributionPlanMutation
from contribution_plan.models import ContributionPlanBundle, ContributionPlan, ContributionPlanBundleDetails
from core.schema import OrderedDjangoFilterConnectionField
from .models import ContributionPlanMutation, ContributionPlanBundleMutation


class Query(graphene.ObjectType):
    contribution_plan = OrderedDjangoFilterConnectionField(
        ContributionPlanGQLType,
        orderBy=graphene.List(of_type=graphene.String),
    )

    contribution_plan_bundle = OrderedDjangoFilterConnectionField(
        ContributionPlanBundleGQLType,
        orderBy=graphene.List(of_type=graphene.String),
        calculation=graphene.UUID(),
        insuranceProduct=graphene.Int(),
    )

    contribution_plan_bundle_details = OrderedDjangoFilterConnectionField(
        ContributionPlanBundleDetailsGQLType,
        orderBy=graphene.List(of_type=graphene.String),
    )

    def resolve_contribution_plan(self, info, **kwargs):
        query = ContributionPlan.objects
        return gql_optimizer.query(query.all(), info)

    def resolve_contribution_plan_bundle(self, info, **kwargs):
        query = ContributionPlanBundle.objects

        calculation = kwargs.get('calculation', None)
        insurance_product = kwargs.get('insuranceProduct', None)

        if calculation:
            query = query.filter(
                contributionplanbundledetails__contribution_plan__calculation__id=str(calculation)
            )

        if insurance_product:
            query = query.filter(
                contributionplanbundledetails__contribution_plan__benefit_plan__id=insurance_product
            )

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

    replace_contribution_plan_bundle = ReplaceContributionPlanBundleMutation.Field()
    replace_contribution_plan = ReplaceContributionPlanMutation.Field()
    replace_contribution_plan_bundle_details = ReplaceContributionPlanBundleDetailsMutation.Field()


def on_contribution_plan_mutation(sender, **kwargs):
    uuid = kwargs['data'].get('uuid', None)
    if not uuid:
        return []
    if "ContributionPlan" in str(sender._mutation_class):
        impacted_contribution_plan = ContributionPlan.objects.get(uuid=uuid)
        ContributionPlanMutation.objects.create(
            contribution_plan=impacted_contribution_plan, mutation_id=kwargs['mutation_log_id'])
    if "ContributionPlanBundle" in str(sender._mutation_class):
        impacted_contribution_plan_bundle = ContributionPlanBundle.objects.get(uuid=uuid)
        ContributionPlanBundleMutation.objects.create(
            contribution_plan_bundle=impacted_contribution_plan_bundle, mutation_id=kwargs['mutation_log_id'])
    return []


def bind_signals():
    signal_mutation_module_validate["contribution_plan"].connect(on_contribution_plan_mutation)