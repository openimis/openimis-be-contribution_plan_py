from core.gql.gql_mutations import DeleteInputType
from core.gql.gql_mutations.base_mutation import BaseDeleteMutation, BaseDeleteMutationMixin, \
    BaseUpdateMutationMixin, BaseMutation, BaseCreateMutationMixin
from contribution_plan.gql.gql_mutations import ContributionPlanInputType
from contribution_plan.models import ContributionPlan


class CreateContributionPlanMutation(BaseMutation, BaseCreateMutationMixin):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(ContributionPlanInputType):
        pass


class DeleteContributionPlanMutation(BaseDeleteMutation, BaseDeleteMutationMixin):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(DeleteInputType):
        pass


class UpdateContributionPlanMutation(BaseMutation, BaseUpdateMutationMixin):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(ContributionPlanInputType):
        pass
