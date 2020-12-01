from datetime import date
from functools import lru_cache
from unittest import TestCase

from contribution_plan.models import ContributionPlanBundle, ContributionPlan, ContributionPlanBundleDetails
from contribution_plan.tests.helpers import create_test_contribution_plan_bundle, create_test_contribution_plan, \
    create_test_contribution_plan_details


class HelpersTest(TestCase):
    """
    Class to check whether the helper methods responsible for creating test data work correctly.
    """

    def test_create_test_contribution_plan_bundle(self):
        contribution_plan_bundle = self.__create_test_contribution_plan_bundle()
        db_contribution_plan_bundle = ContributionPlanBundle.objects.filter(uuid=contribution_plan_bundle.uuid).first()

        self.assertEqual(db_contribution_plan_bundle, contribution_plan_bundle,
                         "Failed to create contribution plan bundle in helper")

    def test_base_create_contribution_plan_bundle_custom_params(self):
        contribution_plan_bundle = self.__create_test_contribution_plan_bundle(custom=True)
        db_contribution_plan_bundle = ContributionPlanBundle.objects.filter(uuid=contribution_plan_bundle.uuid).first()

        params = self.__custom_contribution_plan_bundle_params
        self.assertEqual(db_contribution_plan_bundle.version, params['version'])
        self.assertEqual(db_contribution_plan_bundle.name, params['name'])
        self.assertEqual(db_contribution_plan_bundle.date_updated, params['date_updated'])
        
    def test_create_test_contribution_plan(self):
        contribution_plan = self.__create_test_contribution_plan()
        db_contribution_plan = ContributionPlan.objects.filter(uuid=contribution_plan.uuid).first()

        self.assertEqual(db_contribution_plan, contribution_plan, "Failed to create contribution plan in helper")

    def test_create_contribution_plan_custom_params(self):
        contribution_plan = self.__create_test_contribution_plan(custom=True)
        db_contribution_plan = ContributionPlan.objects.filter(uuid=contribution_plan.uuid).first()

        params = self.__custom_contribution_plan_params
        self.assertEqual(db_contribution_plan.active, params['active'])
        self.assertEqual(db_contribution_plan.code, params['code'])
        self.assertEqual(db_contribution_plan.periodicity, params['periodicity'])     
        
    def test_create_test_contribution_plan_details(self):
        contribution_plan_details = self.__create_test_contribution_plan_details()
        db_contribution_plan_details = ContributionPlanBundleDetails.objects\
            .filter(uuid=contribution_plan_details.uuid).first()

        self.assertEqual(db_contribution_plan_details, contribution_plan_details,
                         "Failed to create contribution plan details in helper")

    def test_base_create_contribution_plan_details_custom_params(self):
        contribution_plan_details = self.__create_test_contribution_plan_details(custom=True)
        db_contribution_plan_details = ContributionPlanBundleDetails.objects\
            .filter(uuid=contribution_plan_details.uuid).first()

        params = self.__custom_contribution_plan_details_params
        self.assertEqual(db_contribution_plan_details.version, params['version'])
        self.assertEqual(db_contribution_plan_details.contribution_plan, params['contribution_plan'])
        self.assertEqual(db_contribution_plan_details.contribution_plan_bundle, params['contribution_plan_bundle'])

    @property
    @lru_cache(maxsize=2)
    def __custom_contribution_plan_bundle_params(self):
        return {
            'version': 1,
            'name': 'Updated CPB',
            'date_updated': date(2011, 10, 31),
            }

    @property
    @lru_cache(maxsize=2)
    def __custom_contribution_plan_params(self):
        return {
            'active': False,
            'code': 'Updated code',
            'periodicity': 4,
            }

    @property
    @lru_cache(maxsize=2)
    def __custom_contribution_plan_details_params(self):
        return {
            'version': 2,
            'contribution_plan': self.__create_test_contribution_plan(True),
            'contribution_plan_bundle': self.__create_test_contribution_plan_bundle(True),
            }

    def __create_test_instance(self, function, **kwargs):
        if kwargs:
            return function(**kwargs)
        else:
            return function()

    def __create_test_contribution_plan_bundle(self, custom=False):
        custom_params = self.__custom_contribution_plan_bundle_params if custom else {}
        return self.__create_test_instance(create_test_contribution_plan_bundle, custom_props=custom_params)

    def __create_test_contribution_plan(self, custom=False):
        custom_params = self.__custom_contribution_plan_params if custom else {}
        return self.__create_test_instance(create_test_contribution_plan, custom_props=custom_params)

    def __create_test_contribution_plan_details(self, custom=False):
        custom_params = self.__custom_contribution_plan_details_params if custom else {}
        return self.__create_test_instance(create_test_contribution_plan_details, custom_props=custom_params)
