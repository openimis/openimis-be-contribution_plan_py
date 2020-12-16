import core
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.contrib.auth.models import AnonymousUser
from django.core import serializers
from django.forms.models import model_to_dict
from contribution_plan.models import ContributionPlan as ContributionPlanModel, ContributionPlanBundle as ContributionPlanBundleModel, \
    ContributionPlanBundleDetails as ContributionPlanBundleDetailsModel


def check_authentication(function):
    def wrapper(self, *args, **kwargs):
        if type(self.user) is AnonymousUser or not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
            }
        else:
            result = function(self, *args, **kwargs)
            return result
    return wrapper


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

    def create(self, contribution_plan_bundle):
        pass

    def update(self, contribution_plan_bundle):
        pass


@core.comparable
class ContributionPlanBundleDetails(object):

    def __init__(self, contribution_plan_bundle_details):
        self.contribution_plan_bundle_details = contribution_plan_bundle_details
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


@core.comparable
class ContributionPlan(object):

    def __init__(self, contribution_plan):
        self.contribution_plan = contribution_plan
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def replace_propagation(self, contribution_plan_bundle):
        pass

    def remove_propagation(self, contribution_plan_bundle):
        pass

    def create(self, contribution_plan):
        pass

    def update(self, contribution_plan):
        pass
