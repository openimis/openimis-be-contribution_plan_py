from core.gql.gql_mutations import DeleteInputType, ReplaceInputType
from core.gql.gql_mutations.base_mutation  import BaseMutation, BaseDeleteMutation, BaseReplaceMutation, \
    BaseHistoryModelCreateMutationMixin, BaseHistoryModelUpdateMutationMixin, \
    BaseHistoryModelDeleteMutationMixin, BaseHistoryModelReplaceMutationMixin
from contribution_plan.gql.gql_mutations import ContributionPlanBundleDetailsInputType, \
    ContributionPlanBundleDetailsUpdateInputType
from contribution_plan.models import ContributionPlanBundleDetails


class CreateContributionPlanBundleDetailsMutation(BaseMutation, BaseHistoryModelCreateMutationMixin):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundleDetails

    class Input(ContributionPlanBundleDetailsInputType):
        pass


class UpdateContributionPlanBundleDetailsMutation(BaseMutation, BaseHistoryModelUpdateMutationMixin):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundleDetails

    class Input(ContributionPlanBundleDetailsUpdateInputType):
        pass


class DeleteContributionPlanBundleDetailsMutation(BaseMutation, BaseHistoryModelDeleteMutationMixin):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundleDetails

    class Input(DeleteInputType):
        pass


class ReplaceContributionPlanMutation(BaseReplaceMutation, BaseHistoryModelReplaceMutationMixin):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundleDetails

    class Input(ReplaceInputType):
        pass