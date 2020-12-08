from core.gql.gql_mutations import DeleteInputType, ReplaceInputType
from core.gql.gql_mutations.base_mutation import BaseMutation, BaseDeleteMutation, BaseReplaceMutation, \
    BaseHistoryModelCreateMutationMixin, BaseHistoryModelUpdateMutationMixin, \
    BaseHistoryModelDeleteMutationMixin, BaseHistoryModelReplaceMutationMixin
from contribution_plan.gql.gql_mutations import ContributionPlanBundleInputType, ContributionPlanBundleUpdateInputType
from contribution_plan.models import ContributionPlanBundle


class CreateContributionPlanBundleMutation(BaseMutation, BaseHistoryModelCreateMutationMixin):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleInputType):
        pass


class UpdateContributionPlanBundleMutation(BaseMutation, BaseHistoryModelUpdateMutationMixin):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleUpdateInputType):
        pass


class DeleteContributionPlanBundleMutation(BaseDeleteMutation, BaseHistoryModelDeleteMutationMixin):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(DeleteInputType):
        pass


class ReplaceContributionPlanMutation(BaseReplaceMutation, BaseHistoryModelReplaceMutationMixin):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(ReplaceInputType):
        pass