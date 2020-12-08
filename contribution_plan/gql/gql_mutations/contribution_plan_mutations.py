from core.gql.gql_mutations import DeleteInputType, ReplaceInputType
from core.gql.gql_mutations.base_mutation import BaseMutation, BaseDeleteMutation, BaseReplaceMutation, \
    BaseHistoryModelCreateMutationMixin, BaseHistoryModelUpdateMutationMixin, \
    BaseHistoryModelDeleteMutationMixin, BaseHistoryModelReplaceMutationMixin
from contribution_plan.gql.gql_mutations import ContributionPlanInputType, ContributionPlanUpdateInputType
from contribution_plan.models import ContributionPlan


class CreateContributionPlanMutation(BaseMutation, BaseHistoryModelCreateMutationMixin):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(ContributionPlanInputType):
        pass


class UpdateContributionPlanMutation(BaseMutation, BaseHistoryModelUpdateMutationMixin):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(ContributionPlanUpdateInputType):
        pass


class DeleteContributionPlanMutation(BaseDeleteMutation, BaseHistoryModelDeleteMutationMixin):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(DeleteInputType):
        pass


class ReplaceContributionPlanMutation(BaseReplaceMutation, BaseHistoryModelReplaceMutationMixin):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(ReplaceInputType):
        pass