import datetime
import numbers
import base64
from unittest import TestCase, mock
from uuid import UUID

import graphene
from contribution_plan.tests.helpers import *
from calculation.tests.helpers import *
from contribution_plan import schema as contribution_plan_schema
from graphene import Schema
from graphene.test import Client


class MutationTestContributionPlan(TestCase):

    class BaseTestContext:
        user = User.objects.get(username="admin")

    class AnonymousUserContext:
        user = mock.Mock(is_anonymous=True)

    @classmethod
    def setUpClass(cls):
        cls.test_contribution_plan_bundle = create_test_contribution_plan_bundle(
            custom_props={'code': 'SuperContributionPlan mutations!'})
        cls.test_contribution_plan = create_test_contribution_plan()
        cls.test_calculation = create_test_calculation_rules()
        cls.test_calculation2 = create_test_calculation_rules()
        cls.test_contribution_plan_details = create_test_contribution_plan_bundle_details()

        cls.schema = Schema(
            query=contribution_plan_schema.Query,
            mutation=contribution_plan_schema.Mutation
        )

        cls.graph_client = Client(cls.schema)

    def test_contribution_plan_create(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "code": "XYZ",
            "name": "XYZ test name xyz - "+str(time_stamp),
            "benefitPlanId": 1,
            "calculationId": f"{self.test_calculation.id}",
            "periodicity": 12,
        }
        self.add_mutation("createContributionPlan", input_param)
        result = self.find_by_exact_attributes_query(
            "contributionPlan",
            params = input_param,
        )["edges"]
        self.assertEqual(
            (
                "XYZ test name xyz - "+str(time_stamp),
                "XYZ",
                1,
                12
            ),
            (
                 result[0]['node']['name'],
                 result[0]['node']['code'],
                 result[0]['node']['version'],
                 result[0]['node']['periodicity']
            )
        )

    def test_contribution_plan_create_date_valid_from_and_date_valid_to(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "code": "XYZ DT",
            "name": "XYZ test date xyz - "+str(time_stamp),
            "dateValidFrom": "2020-12-20",
            "dateValidTo": "2020-12-20",
            "benefitPlanId": 1,
            "calculationId": f"{self.test_calculation.id}",
            "periodicity": 12,
        }
        self.add_mutation("createContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", input_param)["edges"]
        self.assertEqual(
            ( "XYZ test date xyz - "+str(time_stamp),
              "XYZ DT",
              1,
              "2020-12-20T00:00:00",
              "2020-12-20T00:00:00",
              12
            ),
            (
              result[0]['node']['name'],
              result[0]['node']['code'],
              result[0]['node']['version'],
              result[0]['node']['dateValidFrom'],
              result[0]['node']['dateValidTo'],
              result[0]['node']['periodicity']
            )
        )

    def test_contribution_plan_create_without_obligatory_fields(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "name": "XYZ test name xyz - "+str(time_stamp),
        }
        result_mutation = self.add_mutation("createContributionPlan", input_param)
        self.assertEqual(True, 'errors' in result_mutation)

    def test_contribution_plan_delete_more(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "code": "XYZ deletion",
            "name": "XYZ test deletion xyz - "+str(time_stamp),
            "benefitPlanId": 1,
            "calculationId": f"{self.test_calculation.id}",
            "periodicity": 12,
        }
        self.add_mutation("createContributionPlan", input_param)
        self.add_mutation("createContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", {**input_param, 'isDeleted': False})
        converted_ids = [ f"{base64.b64decode(edge['node']['id']).decode('utf-8').split(':')[1]}" for edge in result["edges"] ]

        input_param2 = {
            "uuids": converted_ids,
        }
        self.add_mutation("deleteContributionPlan", input_param2)
        result2 = self.find_by_exact_attributes_query("contributionPlan", {**input_param, 'isDeleted': False})
        self.assertEqual((2, 0), (result["totalCount"], result2["totalCount"]))

    def test_contribution_plan_delete_single_deletion(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "code": "XYZ deletion",
            "name": "XYZ test deletion xyz - "+str(time_stamp),
            "benefitPlanId": 1,
            "calculationId": f"{self.test_calculation.id}",
            "periodicity": 12,
        }
        self.add_mutation("createContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", {**input_param, 'isDeleted': False})
        converted_id = base64.b64decode(result["edges"][0]['node']['id']).decode('utf-8').split(':')[1]
        input_param2 = {
            "uuids": [f"{converted_id}"],
        }
        self.add_mutation("deleteContributionPlan", input_param2)
        result2 = self.find_by_exact_attributes_query("contributionPlan", {**input_param, 'isDeleted': False})
        self.assertEqual((1, 0), (result["totalCount"], result2["totalCount"]))


    def test_contribution_plan_update_1_existing(self):
        id = self.test_contribution_plan.id
        version = self.test_contribution_plan.version
        input_param = {
            "id": f"{id}",
            "name": "XYZ test name xxxxx",
        }
        self.add_mutation("updateContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", {**input_param})["edges"]
        self.test_contribution_plan.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xxxxx", version+1),
            (result[0]['node']['name'], result[0]['node']['version'])
        )

    def test_contribution_plan_update_2_without_changing_fields(self):
        id = self.test_contribution_plan.id
        version = self.test_contribution_plan.version
        input_param = {
            "id": f"{id}",
            "name": "XYZ test name xxxxx",
        }
        self.add_mutation("updateContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", input_param)["edges"]
        self.test_contribution_plan.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xxxxx", version),
            (result[0]['node']['name'], result[0]['node']['version'])
        )

    def test_contribution_plan_update_3_existing_foreign_key(self):
        id = self.test_contribution_plan.id
        version = self.test_contribution_plan.version
        input_param = {
            "id": f"{id}",
            "calculationId": f"{self.test_calculation2.id}",
        }
        self.add_mutation("updateContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", {**input_param})["edges"]
        self.test_contribution_plan.version = result[0]['node']['version']
        self.assertEqual(version+1, result[0]['node']['version'])

    def test_contribution_plan_update_4_without_changing_fields_foreign_key(self):
        id = self.test_contribution_plan.id
        version = self.test_contribution_plan.version
        input_param = {
            "id": f"{id}",
            "calculationId": f"{self.test_calculation2.id}",
        }
        self.add_mutation("updateContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", input_param)["edges"]
        self.test_contribution_plan.version = result[0]['node']['version']
        self.assertEqual(version, result[0]['node']['version'])

    def test_contribution_plan_update_5_existing_date_valid_from_change(self):
        id = self.test_contribution_plan.id
        version = self.test_contribution_plan.version
        input_param = {
            "id": f"{id}",
            "name": "XYZ test name xxxxx",
            "dateValidFrom": "2020-12-09"
        }
        self.add_mutation("updateContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", {**input_param})["edges"]
        self.test_contribution_plan.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xxxxx", version+1, "2020-12-09T00:00:00"),
            (result[0]['node']['name'], result[0]['node']['version'], result[0]['node']['dateValidFrom'])
        )

    def test_contribution_plan_update_6_date_valid_from_without_changing_fields(self):
        id = self.test_contribution_plan.id
        version = self.test_contribution_plan.version
        input_param = {
            "id": f"{id}",
            "name": "XYZ test name xxxxx",
            "dateValidFrom": "2020-12-09"
        }
        self.add_mutation("updateContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", input_param)["edges"]
        self.test_contribution_plan.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xxxxx", version, "2020-12-09T00:00:00"),
            (result[0]['node']['name'], result[0]['node']['version'], result[0]['node']['dateValidFrom'])
        )

    def test_contribution_plan_update_7_without_id_field(self):
        id = self.test_contribution_plan.id
        version = self.test_contribution_plan.version
        input_param = {
            "name": "XYZ test name xxxxx",
        }
        result_mutation = self.add_mutation("updateContributionPlan", input_param)
        self.assertEqual(True, 'errors' in result_mutation)

    def test_contribution_bundle_update_replace(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "code": "XYZ",
            "name": "XYZ test name xyz - " + str(time_stamp),
            "benefitPlanId": 1,
            "calculationId": f"{self.test_calculation.id}",
            "periodicity": 12,
        }
        self.add_mutation("createContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", input_param)["edges"]
        id_record = f"{base64.b64decode(result[0]['node']['id']).decode('utf-8').split(':')[1]}"
        input_param = {
            "uuid": id_record,
        }
        self.add_mutation("replaceContributionPlan", input_param)
        result_replaced = self.find_by_exact_attributes_query("contributionPlan", {"id": id_record})["edges"]
        result_newly_created = self.find_by_exact_attributes_query("contributionPlan", {"id": result_replaced[0]["node"]["replacementUuid"]})["edges"]
        converted_id = base64.b64decode(result_newly_created[0]['node']['id']).decode('utf-8').split(':')[1]
        self.assertEqual(
            (
                True,
                2,
                True,
                result_replaced[0]['node']['replacementUuid'],
                1
            ),
            (
                result_replaced[0]['node']['replacementUuid'] is not None,
                result_replaced[0]['node']['version'],
                result_replaced[0]['node']['dateValidFrom'] is not None,
                converted_id,
                result_newly_created[0]['node']['version']
            )
        )

    def test_contribution_plan_update_replace_twice(self):
        time_stamp = datetime.datetime.now()

        input_param = {
            "code": "XYZ",
            "name": "XYZ test name xyz - " + str(time_stamp),
            "benefitPlanId": 1,
            "calculationId": f"{self.test_calculation.id}",
            "periodicity": 12,
        }

        self.add_mutation("createContributionPlan", input_param)
        result = self.find_by_exact_attributes_query("contributionPlan", input_param)["edges"]
        id_record = f"{base64.b64decode(result[0]['node']['id']).decode('utf-8').split(':')[1]}"

        input_param = {
            "uuid": id_record,
        }

        self.add_mutation("replaceContributionPlan", input_param)
        result_replaced = self.find_by_exact_attributes_query("contributionPlan", {"id": id_record})["edges"]
        result_newly_created = self.find_by_exact_attributes_query("contributionPlan", {
            "id": result_replaced[0]["node"]["replacementUuid"]})["edges"]
        converted_id = base64.b64decode(result_newly_created[0]['node']['id']).decode('utf-8').split(':')[1]

        input_param = {
            "uuid": converted_id,
        }
        self.add_mutation("replaceContributionPlan", input_param)
        result_replaced2 = self.find_by_exact_attributes_query("contributionPlan", {"id": converted_id})["edges"]
        result_newly_created2 = self.find_by_exact_attributes_query("contributionPlan", {
            "id": result_replaced2[0]["node"]["replacementUuid"]})["edges"]
        converted_id2 = base64.b64decode(result_newly_created2[0]['node']['id']).decode('utf-8').split(':')[1]

        self.assertEqual(
            (
                True,
                2,
                True,
                result_replaced2[0]['node']['replacementUuid'],
                1
            ),
            (
                result_replaced2[0]['node']['replacementUuid'] is not None,
                result_replaced2[0]['node']['version'],
                result_replaced2[0]['node']['dateValidFrom'] is not None,
                converted_id2,
                result_newly_created2[0]['node']['version']
            )
        )

    def find_by_id_query(self, query_type, id, context=None):
        query = F'''
        {{
            {query_type}(id:"{id}") {{
                totalCount
                edges {{
                  node {{
                    id
                    version
                  }}
                  cursor
                }}
          }}
        }}
        '''

        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]['edges']

        if len(records) > 1:
            raise ValueError(F"Ambiguous id {id} for query {query_type}")

        return records

    def find_by_exact_attributes_query(self, query_type, params, context=None):
        if "dateValidFrom" in params:
            params.pop('dateValidFrom')
        if "dateValidTo" in params:
            params.pop('dateValidTo')
        if "benefitPlanId" in params:
            params.pop('benefitPlanId')
        if "calculationId" in params:
            params.pop('calculationId')
        node_content_str = "\n".join(params.keys())
        query = F'''
        {{
            {query_type}({self.build_params(params)}) {{
                totalCount
                edges {{
                  node {{
                    {'id' if 'id' not in params else '' }
                    {node_content_str}
                    version
                    dateValidFrom
                    dateValidTo
                    replacementUuid
                  }}
                  cursor
                }}
          }}
        }}
        '''
        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]
        return records

    def execute_query(self, query, context=None):
        if context is None:
            context = self.BaseTestContext()

        query_result = self.graph_client.execute(query, context=context)
        query_data = query_result['data']
        return query_data

    def add_mutation(self, mutation_type, input_params, context=None):
        mutation = f'''
        mutation 
        {{
            {mutation_type}(input: {{
               {self.build_params(input_params)}
            }})  

          {{
            internalId
            clientMutationId
          }}
        }}
        '''
        mutation_result = self.execute_mutation(mutation, context=context)
        return mutation_result

    def execute_mutation(self, mutation, context=None):
        if context is None:
            context = self.BaseTestContext()

        mutation_result = self.graph_client.execute(mutation, context=context)
        return mutation_result

    def build_params(self, params):
        def wrap_arg(v):
            if isinstance(v, str):
                return F'"{v}"'
            if isinstance(v, list):
                return json.dumps(v)
            if isinstance(v, bool):
                return str(v).lower()
            if isinstance(v, datetime.date):
                return graphene.DateTime.serialize(
                    datetime.datetime.fromordinal(v.toordinal()))
            return v

        params_as_args = [f'{k}:{wrap_arg(v)}' for k, v in params.items()]
        return ", ".join(params_as_args)