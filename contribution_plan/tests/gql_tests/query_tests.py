import datetime
import numbers
from unittest import TestCase, mock
from uuid import UUID

import graphene
from contribution_plan.tests.helpers import *
from contribution_plan import schema as contribution_plan_schema
from graphene import Schema
from graphene.test import Client


class QueryTest(TestCase):

    class BaseTestContext:
        user = mock.Mock(is_anonymous=False)
        user.has_perm = mock.MagicMock(return_value=False)

    class AnonymousUserContext:
        user = mock.Mock(is_anonymous=True)

    @classmethod
    def setUpClass(cls):
        cls.test_contribution_plan_bundle = create_test_contribution_plan_bundle(
            custom_props={'code': 'SuperContributionPlan!'})
        cls.test_contribution_plan_bundle.save()
        cls.test_contribution_plan = create_test_contribution_plan()
        cls.test_contribution_plan_details = create_test_contribution_plan_bundle_details()

        cls.schema = Schema(
            query=contribution_plan_schema.Query,
            mutation=contribution_plan_schema.Mutation
        )

        cls.graph_client = Client(cls.schema)

    def test_find_contribution_plan_bundle_existing(self):
        uuid = self.test_contribution_plan_bundle.uuid
        result = self.find_by_uuid_query("contributionPlanBundle", uuid)
        self.assertEqual(UUID(result[0]['node']['uuid']), uuid)

    def test_find_contribution_plan_existing(self):
        uuid = self.test_contribution_plan.uuid
        result = self.find_by_uuid_query("contributionPlan", uuid)
        self.assertEqual(UUID(result[0]['node']['uuid']), uuid)

    def test_find_contribution_plan_details_existing(self):
        uuid = self.test_contribution_plan_details.uuid
        result = self.find_by_uuid_query("contributionPlanBundleDetails", uuid)
        self.assertEqual(UUID(result[0]['node']['uuid']), uuid)

    def test_find_contribution_plan_bundle_by_params(self):
        expected = self.test_contribution_plan_bundle
        params = {'version': expected.version, 'active': expected.active, 'code': expected.code,
                  'name': expected.name, 'dateCreated': expected.date_created}
        result = self.find_by_exact_attributes_query("contributionPlanBundle", params)
        self.assertDictEqual()

    def test_find_contribution_plan_bundle_existing_anonymous_user(self):
        result_cpb = self.find_by_uuid_query("contributionPlanBundle",
                                         self.test_contribution_plan_bundle.uuid,
                                         context=self.AnonymousUserContext())
        result_cp = self.find_by_uuid_query("contributionPlan",
                                         self.test_contribution_plan.uuid,
                                         context=self.AnonymousUserContext())
        result_cpbd = self.find_by_uuid_query("contributionPlanBundleDetails",
                                         self.test_contribution_plan_details.uuid,
                                         context=self.AnonymousUserContext())

        self.assertEqual(len(result_cp), 0)
        self.assertEqual(len(result_cpb), 0)
        self.assertEqual(len(result_cpbd), 0)

    def test_find_contribution_plan_details_by_contribution(self):
        details_contribution_bundle_uuid = self.test_contribution_plan_details.contribution_plan_bundle.uuid
        details_contribution_plan_uuid = self.test_contribution_plan_details.contribution_plan.uuid
        uuid = self.test_contribution_plan_details.uuid
        query = F'''
        {{
            contributionPlanBundleDetails(
                contributionPlan_Uuid:"{details_contribution_plan_uuid}",
                contributionPlanBundle_Uuid:"{details_contribution_bundle_uuid}") {{
                totalCount
                edges {{
                  node {{
                    uuid
                  }}
                  cursor
                }}
          }}
        }}
        '''
        query_result = self.execute_query(query)
        result = query_result['contributionPlanBundleDetails']['edges'][0]['node']
        self.assertEqual(UUID(result['uuid']), uuid)

    def find_by_uuid_query(self, query_type, uuid, context=None):
        query = F'''
        {{
            {query_type}(uuid:"{uuid}") {{
                totalCount
                edges {{
                  node {{
                    uuid
                  }}
                  cursor
                }}
          }}
        }}
        '''

        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]['edges']

        if len(records) > 1:
            raise ValueError(F"Ambiguous uuid {uuid} for query {query_type}")

        return records

    def find_by_exact_attributes_query(self, query_type, params, context=None):
        node_content_str = "\n".join(params.keys())
        query = F'''
        {{
            {query_type}({self.build_params(params)}) {{
                totalCount
                edges {{
                  node {{
                    {node_content_str}
                  }}
                  cursor
                }}
          }}
        }}
        '''
        print(query)
        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]['edges']
        return records

    def execute_query(self, query, context=None):
        if context is None:
            context = self.BaseTestContext()

        query_result = self.graph_client.execute(query, context=context)
        print(query_result)
        query_data = query_result['data']
        return query_data

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
