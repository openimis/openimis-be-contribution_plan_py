import json

from unittest import TestCase
from contribution_plan.services import ContributionPlan as ContributionPlanService, ContributionPlanBundle as ContributionPlanBundleService, \
    ContributionPlanBundleDetails as ContributionPlanBundleDetailsService
from contribution_plan.models import ContributionPlan, ContributionPlanBundle, ContributionPlanBundleDetails
from calculation.models import CalculationRules
from product.models import Product
from core.models import User

from product.test_helpers import create_test_product
from calculation.tests.helpers_tests import create_test_calculation_rules


class ServiceTestContributionPlan(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.get(username="admin")
        cls.contribution_plan_service = ContributionPlanService(cls.user)
        #cls.contribution_plan_bundle_service = ContributionPlanBundleService(cls.user)
        #cls.contribution_plan_bundle_details_service = ContributionPlanBundleDetailsService(cls.user)

    def test_contribution_plan_create(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERVICE",
            'name': "Contribution Plan Name Service",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        self.assertEqual(
            (
                 True,
                 "Ok",
                 "",
                 "CP SERVICE",
                 "Contribution Plan Name Service",
                 1,
                 6,
                 product.id,
                 str(calculation.id),
            ),
            (
                 response['success'],
                 response['message'],
                 response['detail'],
                 response['data']['code'],
                 response['data']['name'],
                 response['data']['version'],
                 response['data']['periodicity'],
                 response['data']['benefit_plan'],
                 response['data']['calculation'],
            )
        )

    def test_contribution_plan_create_update(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])
        contribution_plan_to_update = {
            'id': str(contribution_plan_object.id),
            'periodicity': 12,
        }
        response = self.contribution_plan_service.update(contribution_plan_to_update)
        self.assertEqual(
            (
                True,
                "Ok",
                "",
                12,
                2,
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response['data']['periodicity'],
                response['data']['version'],
            )
        )

    def test_contribution_plan_create_update_benefit_plan(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])

        product_first_id = Product.objects.order_by('id').first()

        contribution_plan_to_update = {
            'id': str(contribution_plan_object.id),
            'periodicity': 12,
            'benefit_plan_id': product_first_id.id,
        }
        response = self.contribution_plan_service.update(contribution_plan_to_update)
        self.assertEqual(
            (
                True,
                "Ok",
                "",
                12,
                2,
                product_first_id.id,
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response['data']['periodicity'],
                response['data']['version'],
                response['data']['benefit_plan']
            )
        )

    def test_contribution_plan_create_update_calculation(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])

        calculation_first = CalculationRules.objects.order_by('id').first()

        contribution_plan_to_update = {
            'id': str(contribution_plan_object.id),
            'periodicity': 12,
            'calculation_id': str(calculation_first.id),
        }
        response = self.contribution_plan_service.update(contribution_plan_to_update)
        self.assertEqual(
            (
                True,
                "Ok",
                "",
                12,
                2,
                str(calculation_first.id)
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response['data']['periodicity'],
                response['data']['version'],
                response['data']['calculation'],
            )
        )

    def test_contribution_plan_create_update_both_fk(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])

        product_first_id = Product.objects.order_by('id').first()
        calculation_first = CalculationRules.objects.order_by('id').first()

        contribution_plan_to_update = {
            'id': str(contribution_plan_object.id),
            'periodicity': 12,
            'benefit_plan_id': product_first_id.id,
            'calculation_id': str(calculation_first.id),
        }
        response = self.contribution_plan_service.update(contribution_plan_to_update)
        self.assertEqual(
            (
                True,
                "Ok",
                "",
                12,
                2,
                product_first_id.id,
                str(calculation_first.id)
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response['data']['periodicity'],
                response['data']['version'],
                response['data']['benefit_plan'],
                response['data']['calculation'],
            )
        )

    def test_contribution_plan_update_without_changing_field(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CPUWCF",
            'name': "CP for update without changing fields",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_to_update = {
            'id': str(response["data"]["id"]),
            'periodicity': 6,
        }

        response = self.contribution_plan_service.update(contribution_plan_to_update)
        self.assertEqual(
            (
                False,
                "Failed to update ContributionPlan",
                "['Record has not be updated - there are no changes in fields']",
            ),
            (
                response['success'],
                response['message'],
                response['detail']
            )
        )

    def test_contribution_plan_update_without_id(self):
        policy_holder = {
            'periodicity': 6,
        }
        response = self.contribution_plan_service.update(policy_holder)
        self.assertEqual(
            (
                False,
                "Failed to update ContributionPlan",
            ),
            (
                response['success'],
                response['message'],
            )
        )

    def test_contribution_plan_replace(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': str(product.id),
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])

        contribution_plan_to_replace = {
            'uuid': str(contribution_plan_object.id),
            'periodicity': 3,
        }

        response = self.contribution_plan_service.replace(contribution_plan_to_replace)
        contribution_plan_new_replaced_object = ContributionPlan.objects.get(id=response['uuid_new_object'])
        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
                3
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
                contribution_plan_new_replaced_object.periodicity
            )
        )

    def test_contribution_plan_replace_product(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])

        product_first_id = Product.objects.order_by('id').first()

        contribution_plan_to_replace = {
            'uuid': str(contribution_plan_object.id),
            'periodicity': 3,
            'benefit_plan_id': str(product_first_id.id)
        }

        response = self.contribution_plan_service.replace(contribution_plan_to_replace)
        contribution_plan_new_replaced_object = ContributionPlan.objects.get(id=response['uuid_new_object'])
        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
                3,
                product_first_id.id
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
                contribution_plan_new_replaced_object.periodicity,
                contribution_plan_new_replaced_object.benefit_plan.id,
            )
        )

    def test_contribution_plan_replace_calculation(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])

        calculation_first = CalculationRules.objects.order_by('id').first()

        contribution_plan_to_replace = {
            'uuid': str(contribution_plan_object.id),
            'periodicity': 3,
            'calculation_id': str(calculation_first.id)
        }

        response = self.contribution_plan_service.replace(contribution_plan_to_replace)
        contribution_plan_new_replaced_object = ContributionPlan.objects.get(id=response['uuid_new_object'])
        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
                3,
                str(calculation_first.id)
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
                contribution_plan_new_replaced_object.periodicity,
                str(contribution_plan_new_replaced_object.calculation.id),
            )
        )

    def test_contribution_plan_replace_both_fk(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)
        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])

        product_first_id = Product.objects.order_by('id').first()
        calculation_first = CalculationRules.objects.order_by('id').first()

        contribution_plan_to_replace = {
            'uuid': str(contribution_plan_object.id),
            'periodicity': 3,
            'benefit_plan_id': product_first_id.id,
            'calculation_id': str(calculation_first.id),
        }

        response = self.contribution_plan_service.replace(contribution_plan_to_replace)
        contribution_plan_new_replaced_object = ContributionPlan.objects.get(id=response['uuid_new_object'])
        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
                3,
                product_first_id.id,
                str(calculation_first.id),
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
                contribution_plan_new_replaced_object.periodicity,
                contribution_plan_new_replaced_object.benefit_plan.id,
                str(contribution_plan_new_replaced_object.calculation.id),
            )
        )

    def test_contribution_plan_replace_double(self):
        product = create_test_product("PCODE")
        calculation = create_test_calculation_rules()

        contribution_plan = {
            'code': "CP SERUPD",
            'name': "CP for update",
            'benefit_plan_id': product.id,
            'periodicity': 6,
            'calculation_id': str(calculation.id),
            'json_ext': json.dumps("{}"),
        }

        response = self.contribution_plan_service.create(contribution_plan)

        contribution_plan_object = ContributionPlan.objects.get(id=response['data']['id'])
        contribution_plan_to_replace = {
            'uuid': str(contribution_plan_object.id),
            'periodicity': 3,
        }
        response = self.contribution_plan_service.replace(contribution_plan_to_replace)
        contribution_plan_new_replaced_object = ContributionPlan.objects.get(id=response['uuid_new_object'])

        product_first_id = Product.objects.order_by('id').first()

        contribution_plan_object = ContributionPlan.objects.get(id=response['uuid_new_object'])
        contribution_plan_to_replace_again = {
            'uuid': str(contribution_plan_object.id),
            'periodicity': 2,
            'benefit_plan_id': product_first_id.id,
        }

        response = self.contribution_plan_service.replace(contribution_plan_to_replace_again)
        contribution_plan_new_replaced_object2 = ContributionPlan.objects.get(id=response['uuid_new_object'])

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
                3,
                2,
                product_first_id.id,
                1,
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
                contribution_plan_new_replaced_object.periodicity,
                contribution_plan_new_replaced_object2.periodicity,
                contribution_plan_new_replaced_object2.benefit_plan.id,
                contribution_plan_new_replaced_object2.version
            )
        )