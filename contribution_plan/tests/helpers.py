import json
from functools import lru_cache

from contribution_plan.models import ContributionPlanBundle, ContributionPlan, ContributionPlanBundleDetails
from datetime import date

from core.models import InteractiveUser, User
from product.test_helpers import create_test_product


def create_test_contribution_plan_bundle(custom_props={}):
    user = __get_or_create_simple_contribution_plan_user()
    object_data = {
        'is_deleted': 0,
        'code': "Contribution Plan Bundle Code",
        'name': "Contribution Plan Bundle Name",
        'json_ext': json.dumps("{}"),
        **custom_props
    }

    contribution_plan_bundle = ContributionPlanBundle(**object_data)
    contribution_plan_bundle.save(username=user.username)

    return contribution_plan_bundle


def create_test_contribution_plan(product=None, custom_props={}):
    if not product:
        product = create_test_product("PlanCode")

    user = __get_or_create_simple_contribution_plan_user()

    object_data = {
        'is_deleted': False,
        'code': "Contribution Plan Code",
        'name': "Contribution Plan Name",
        'benefit_plan': product,
        'periodicity': 12,
        'json_ext': json.dumps("{}"),
        **custom_props
    }

    contribution_plan = ContributionPlan(**object_data)
    contribution_plan.save(username=user.username)

    return contribution_plan


def create_test_contribution_plan_bundle_details(contribution_plan_bundle=None, contribution_plan=None,
                                                 custom_props={}):
    if not contribution_plan_bundle:
        contribution_plan_bundle = create_test_contribution_plan_bundle()

    if not contribution_plan:
        contribution_plan = create_test_contribution_plan()

    user = __get_or_create_simple_contribution_plan_user()
    object_data = {
        'contribution_plan_bundle': contribution_plan_bundle,
        'contribution_plan': contribution_plan,
        'json_ext': json.dumps("{}"),
        'date_created': date(2010, 10, 30),
        'user_updated': user,
        'user_created': user,
        'date_valid_from': date(2010, 10, 30),
        'date_valid_to': None,
        'is_deleted': 0,
        **custom_props
    }

    contribution_plan_bundle_details = ContributionPlanBundleDetails(**object_data)
    contribution_plan_bundle_details.save(username=user.username)

    return contribution_plan_bundle_details


def __get_or_create_simple_contribution_plan_user():
    user = User.objects.get(username="admin")
    return user
