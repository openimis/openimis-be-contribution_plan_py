import core


@core.comparable
class ContributionPlanBundle(object):

    def __init__(self, contribution_plan_bundle):
        self.contribution_plan_bundle = contribution_plan_bundle
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def replace_propagation(self, policy_holder):
        pass

    def remove_propagation(self, policy_holder):
        pass


@core.comparable
class ContributionPlanBundleDetails(object):

    def __init__(self, contribution_plan_bundle_details):
        self.contribution_plan_bundle_details = contribution_plan_bundle_details
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


@core.comparable
class ContributionPlanBundle(object):

    def __init__(self, contribution_plan):
        self.contribution_plan = contribution_plan
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
