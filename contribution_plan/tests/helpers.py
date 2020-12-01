import json
from functools import lru_cache

from contribution_plan.models import ContributionPlanBundle, ContributionPlan, ContributionPlanBundleDetails
from datetime import date

from core.models import InteractiveUser, User
from product.test_helpers import create_test_product


def create_test_contribution_plan_bundle(custom_props={}):
    user = __get_or_create_simple_contribution_plan_user()
    object_data = {
        'version': 1,
        'active': True,
        'code': "Contribution Plan Bundle Code",
        'name': "Contribution Plan Bundle Name",
        'json_ext': json.dumps("{}"),
        'date_created': date(2010, 10, 30),
        'date_updated': date(2010, 10, 31),
        'user_updated': user,
        'user_created': user,
        'date_valid_from': date(2010, 10, 30),
        'date_valid_to': None,
        **custom_props
    }
    return ContributionPlanBundle.objects.create(**object_data)


def create_test_contribution_plan(product=None, custom_props={}):
    if not product:
        product = create_test_product("PlanCode")

    user = __get_or_create_simple_contribution_plan_user()

    object_data = {
        'version': 1,
        'active': True,
        'code': "Contribution Plan Code",
        'benefit_plan': product,
        'periodicity': 12,
        'json_ext': json.dumps("{}"),
        'date_created': date(2010, 10, 30),
        'amendment': 12,
        'date_updated': date(2010, 10, 31),
        'user_updated': user,
        'user_created': user,
        'date_valid_from': date(2010, 10, 30),
        'date_valid_to': None,
        **custom_props
    }
    
    return ContributionPlan.objects.create(**object_data)


def create_test_contribution_plan_bundle_details(contribution_plan_bundle=None, contribution_plan=None,
                                                 custom_props={}):
    if not contribution_plan_bundle:
        contribution_plan_bundle = create_test_contribution_plan_bundle()

    if not contribution_plan:
        contribution_plan = create_test_contribution_plan()

    user = __get_or_create_simple_contribution_plan_user()
    object_data = {
        'version': 1,
        'contribution_plan_bundle': contribution_plan_bundle,
        'contribution_plan': contribution_plan,
        'json_ext': json.dumps("{}"),
        'date_created': date(2010, 10, 30),
        'user_updated': user,
        'user_created': user,
        'date_valid_from': date(2010, 10, 30),
        'date_valid_to': None,
        'active': 1,
        **custom_props
    }

    return ContributionPlanBundleDetails.objects.create(**object_data)


def __get_or_create_simple_contribution_plan_user():
    user = User.objects.get(username="admin")
    #user, _ = User.objects.get_or_create(username='contribution_plan_user',
    #                                     i_user=InteractiveUser.objects.first())
    return user
