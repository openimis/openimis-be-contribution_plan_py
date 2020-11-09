from contribution_plan.gql.gql_mutations import ContributionPlanBundleInputType
from contribution_plan.gql.gql_mutations.base_mutation import BaseDeleteMutation, BaseDeleteMutationMixin, \
    BaseUpdateMutationMixin, BaseMutation, BaseCreateMutationMixin
from contribution_plan.models import ContributionPlanBundle


class CreateContributionPlanBundleMutation(BaseMutation, BaseCreateMutationMixin):
    _mutation_class = "ContributionPlanBundleMutation"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleInputType):
        pass


class DeleteContributionPlanBundleMutation(BaseDeleteMutation, BaseDeleteMutationMixin):
    _mutation_class = "ContributionPlanBundleMutation"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleInputType):
        pass


class UpdateContributionPlanBundleMutation(BaseMutation, BaseUpdateMutationMixin):
    _mutation_class = "ContributionPlanBundleMutation"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleInputType):
        pass
