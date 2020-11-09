from contribution_plan.gql.gql_mutations import ContributionPlanBundleDetailsInputType
from contribution_plan.gql.gql_mutations.base_mutation import BaseDeleteMutationMixin, BaseUpdateMutationMixin, \
    BaseMutation, BaseCreateMutationMixin
from contribution_plan.models import ContributionPlanBundleDetails


class CreateContributionPlanBundleDetailsMutation(BaseMutation, BaseCreateMutationMixin):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _model = ContributionPlanBundleDetails

    def _validate_mutation(cls, user, **data):
        user.hasPerm('sdasdo')
    class Input(ContributionPlanBundleDetailsInputType):
        pass


class DeleteContributionPlanBundleDetailsMutation(BaseMutation, BaseDeleteMutationMixin):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _model = ContributionPlanBundleDetails

    class Input(ContributionPlanBundleDetailsInputType):
        pass


class UpdateContributionPlanBundleDetailsMutation(BaseMutation, BaseUpdateMutationMixin):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _model = ContributionPlanBundleDetails

    class Input(ContributionPlanBundleDetailsInputType):
        pass