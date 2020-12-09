import datetime
import numbers
import base64
from unittest import TestCase, mock
from uuid import UUID

import graphene
from contribution_plan.tests.helpers import *
from contribution_plan import schema as contribution_plan_schema
from graphene import Schema
from graphene.test import Client


class MutationTest(TestCase):

    class BaseTestContext:
        user = User.objects.get(username="admin")

    class AnonymousUserContext:
        user = mock.Mock(is_anonymous=True)

    @classmethod
    def setUpClass(cls):
        cls.test_contribution_plan_bundle = create_test_contribution_plan_bundle(
            custom_props={'code': 'SuperContributionPlan mutations!'})
        cls.test_contribution_plan = create_test_contribution_plan()
        cls.test_contribution_plan_details = create_test_contribution_plan_bundle_details()

        cls.schema = Schema(
            query=contribution_plan_schema.Query,
            mutation=contribution_plan_schema.Mutation
        )

        cls.graph_client = Client(cls.schema)

    def test_create_contribution_plan_bundle(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "code": "XYZ",
            "name": "XYZ test name xyz - "+str(time_stamp),
        }
        result_mutation = self.add_mutation("createContributionPlanBundle", input_param)
        result = self.find_by_exact_attributes_query("contributionPlanBundle", input_param)
        self.test_contribution_plan_bundle.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xyz - "+str(time_stamp), "XYZ", 1),
            (result[0]['node']['name'], result[0]['node']['code'], result[0]['node']['version'])
        )

    def test_create_contribution_plan_bundle_without_obligatory_fields(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "name": "XYZ test name xyz - "+str(time_stamp),
        }
        result_mutation = self.add_mutation("createContributionPlanBundle", input_param)
        self.assertEqual(True, 'errors' in result_mutation)

    def test_update_contribution_plan_bundle_1_existing(self):
        id = self.test_contribution_plan_bundle.id
        version = self.test_contribution_plan_bundle.version
        input_param = {
            "id": f"{id}",
            "name": "XYZ test name xxxxx",
        }
        result_mutation = self.add_mutation("updateContributionPlanBundle", input_param)
        result = self.find_by_exact_attributes_query("contributionPlanBundle", {**input_param})
        self.test_contribution_plan_bundle.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xxxxx", version+1),
            (result[0]['node']['name'], result[0]['node']['version'])
        )

    def test_update_contribution_plan_bundle_2_without_changing_fields(self):
        id = self.test_contribution_plan_bundle.id
        version = self.test_contribution_plan_bundle.version
        input_param = {
            "id": f"{id}",
            "name": "XYZ test name xxxxx",
        }
        result_mutation = self.add_mutation("updateContributionPlanBundle", input_param)
        result = self.find_by_exact_attributes_query("contributionPlanBundle", input_param)
        self.test_contribution_plan_bundle.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xxxxx", version),
            (result[0]['node']['name'], result[0]['node']['version'])
        )

    def test_update_contribution_plan_bundle_3_existing_date_valid_from_change(self):
        id = self.test_contribution_plan_bundle.id
        version = self.test_contribution_plan_bundle.version
        input_param = {
            "id": f"{id}",
            "name": "XYZ test name xxxxx",
            "dateValidFrom": "2020-12-09"
        }
        result_mutation = self.add_mutation("updateContributionPlanBundle", input_param)
        result = self.find_by_exact_attributes_query("contributionPlanBundle", {**input_param})
        self.test_contribution_plan_bundle.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xxxxx", version+1, "2020-12-09T00:00:00"),
            (result[0]['node']['name'], result[0]['node']['version'], result[0]['node']['dateValidFrom'])
        )

    def test_update_contribution_plan_bundle_4_date_valid_from_without_changing_fields(self):
        id = self.test_contribution_plan_bundle.id
        version = self.test_contribution_plan_bundle.version
        input_param = {
            "id": f"{id}",
            "name": "XYZ test name xxxxx",
            "dateValidFrom": "2020-12-09"
        }
        result_mutation = self.add_mutation("updateContributionPlanBundle", input_param)
        result = self.find_by_exact_attributes_query("contributionPlanBundle", input_param)
        self.test_contribution_plan_bundle.version = result[0]['node']['version']
        self.assertEqual(
            ("XYZ test name xxxxx", version, "2020-12-09T00:00:00"),
            (result[0]['node']['name'], result[0]['node']['version'], result[0]['node']['dateValidFrom'])
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

    def find_by_exact_attributes_query(self, query_type, params, foreign_key="", context=None):
        if "dateValidFrom" in params:
            params.pop('dateValidFrom')
        if "dateValidTo" in params:
            params.pop('dateValidTo')
        node_content_str = "\n".join(params.keys())
        query = F'''
        {{
            {query_type}({self.build_params(params)}) {{
                totalCount
                edges {{
                  node {{
                    {node_content_str}
                    version
                    dateValidFrom
                    dateValidTo 
                    {foreign_key}
                  }}
                  cursor
                }}
          }}
        }}
        '''
        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]['edges']
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
            if isinstance(v, bool):
                return str(v).lower()
            if isinstance(v, datetime.date):
                return graphene.DateTime.serialize(
                    datetime.datetime.fromordinal(v.toordinal()))
                # return F'"{datetime.datetime.fromordinal()}"'
            return v  # if isinstance(v, numbers.Number) else F'"{v}"'

        params_as_args = [f'{k}:{wrap_arg(v)}' for k, v in params.items()]
        return ", ".join(params_as_args)