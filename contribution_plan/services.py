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


class ContributionPlanBundle(object):

    def __init__(self, user):
        self.user = user

    @check_authentication
    def get_by_id(self, by_contribution_plan_bundle):
        try:
            ph = ContributionPlanBundleModel.objects.get(id=by_contribution_plan_bundle.id)
            uuid_string = str(ph.id)
            dict_representation = model_to_dict(ph)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="ContributionPlanBundle", method="get", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def create(self, contribution_plan_bundle):
        try:
            cpb = ContributionPlanBundleModel(**contribution_plan_bundle)
            cpb.save(username=self.user.username)
            uuid_string = str(cpb.id)
            dict_representation = model_to_dict(cpb)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="ContributionPlanBundle", method="create", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def update(self, contribution_plan_bundle):
        try:
            updated_cpb = ContributionPlanBundleModel.objects.filter(id=contribution_plan_bundle['id']).first()
            [setattr(updated_cpb, key, contribution_plan_bundle[key]) for key in contribution_plan_bundle]
            updated_cpb.save(username=self.user.username)
            uuid_string = str(updated_cpb.id)
            dict_representation = model_to_dict(updated_cpb)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="ContributionPlanBundle", method="update", exception=exc)
        return _output_result_success(dict_representation=dict_representation)

    @check_authentication
    def delete(self, contribution_plan_bundle):
        try:
            cpb_to_delete = ContributionPlanBundleModel.objects.filter(id=contribution_plan_bundle['id']).first()
            cpb_to_delete.delete(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": "",
            }
        except Exception as exc:
            return _output_exception(model_name="ContributionPlanBundle", method="delete", exception=exc)

    @check_authentication
    def replace(self, contribution_plan_bundle):
        try:
            cpb_to_replace = ContributionPlanBundleModel.objects.filter(id=contribution_plan_bundle['uuid']).first()
            cpb_to_replace.replace_object(data=contribution_plan_bundle, username=self.user.username)
            uuid_string = str(cpb_to_replace.id)
            dict_representation = model_to_dict(cpb_to_replace)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return _output_exception(model_name="ContributionPlanBundle", method="replace", exception=exc)
        return {
            "success": True,
            "message": "Ok",
            "detail": "",
            "old_object": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
            "uuid_new_object": str(cpb_to_replace.replacement_uuid),
        }

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


def _output_exception(model_name, method, exception):
    return {
        "success": False,
        "message": f"Failed to {method} {model_name}",
        "detail": str(exception),
        "data": "",
    }


def _output_result_success(dict_representation):
    return {
        "success": True,
        "message": "Ok",
        "detail": "",
        "data": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
    }
