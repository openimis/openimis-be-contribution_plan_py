"""The "Show deleted" filter on contribution plan bundles and their details.

The list resolvers decide the soft-delete scope through append_validity_filter:
deleted rows are hidden by default, returned with isDeleted: true, and a lookup
by id finds the record whatever its state (OP-3256). A model get_queryset that
forces is_deleted=False on top of that turns isDeleted: true into
is_deleted=True AND is_deleted=False, an empty list (follow-up of OP-3180).
"""
import base64
from uuid import UUID

from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from contribution_plan import schema as contribution_plan_schema
from contribution_plan.gql.gql_mutations.contribution_plan_bundle_details_mutations import (
    UpdateContributionPlanBundleDetailsMutation,
)
from contribution_plan.gql.gql_mutations.contribution_plan_bundle_mutations import (
    ReplaceContributionPlanBundleMutation,
    UpdateContributionPlanBundleMutation,
)
from contribution_plan.models import ContributionPlanBundle, ContributionPlanBundleDetails
from contribution_plan.tests.helpers import (
    create_test_contribution_plan_bundle,
    create_test_contribution_plan_bundle_details,
)
from core.models.openimis_graphql_test_case import BaseTestContext
from core.test_helpers import create_test_interactive_user


class ShowDeletedTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_test_interactive_user(username="cpShowDeleted")
        cls.live_bundle = create_test_contribution_plan_bundle(custom_props={"code": "SD-LIVE"})
        cls.deleted_bundle = create_test_contribution_plan_bundle(custom_props={"code": "SD-DEL"})
        cls.live_details = create_test_contribution_plan_bundle_details(
            contribution_plan_bundle=cls.live_bundle)
        cls.deleted_details = create_test_contribution_plan_bundle_details(
            contribution_plan_bundle=cls.live_bundle)
        cls.deleted_bundle.delete(username=cls.user.username)
        cls.deleted_details.delete(username=cls.user.username)

    def setUp(self):
        self.client_gql = Client(Schema(query=contribution_plan_schema.Query))
        self.context = BaseTestContext(self.user).get_request()

    def _ids(self, field, args):
        args = f"({args})" if args else ""
        query = f"{{ {field}{args} {{ edges {{ node {{ id }} }} }} }}"
        result = self.client_gql.execute(query, context=self.context)
        self.assertIsNone(result.get("errors"), result.get("errors"))
        return {
            UUID(base64.b64decode(edge["node"]["id"]).decode("utf-8").split(":")[1])
            for edge in result["data"][field]["edges"]
        }

    def _check(self, field, live, deleted, extra=""):
        sep = ", " if extra else ""
        shown = self._ids(field, f"isDeleted: true{sep}{extra}")
        self.assertIn(deleted.id, shown, "isDeleted: true must return the soft-deleted row")
        self.assertNotIn(live.id, shown, "isDeleted: true must not return live rows")

        default = self._ids(field, extra)
        self.assertIn(live.id, default, "the default list must return live rows")
        self.assertNotIn(deleted.id, default, "the default list must hide soft-deleted rows")

        by_id = self._ids(field, f'id: "{deleted.id}"')
        self.assertEqual(by_id, {deleted.id}, "a lookup by id must find a soft-deleted row (OP-3256)")

    def test_contribution_plan_bundle_show_deleted(self):
        self._check("contributionPlanBundle", self.live_bundle, self.deleted_bundle)

    def test_contribution_plan_bundle_details_show_deleted(self):
        self._check(
            "contributionPlanBundleDetails", self.live_details, self.deleted_details,
            extra=f'contributionPlanBundle_Id: "{self.live_bundle.id}"',
        )

    # Mutations look their target up through get_queryset (core target_queryset).
    # Showing deleted rows must not make them writable.

    def test_update_refuses_deleted_bundle(self):
        errors = UpdateContributionPlanBundleMutation.async_mutate(
            self.user, id=self.deleted_bundle.id, name="changed")
        self.assertTrue(errors)
        self.assertNotEqual(ContributionPlanBundle.objects.get(id=self.deleted_bundle.id).name, "changed")

    def test_replace_refuses_deleted_bundle(self):
        errors = ReplaceContributionPlanBundleMutation.async_mutate(
            self.user, uuid=self.deleted_bundle.id, code="SD-DEL-R", name="replacement")
        self.assertTrue(errors)
        self.assertIsNone(ContributionPlanBundle.objects.get(id=self.deleted_bundle.id).replacement_uuid)

    def test_update_refuses_deleted_bundle_details(self):
        errors = UpdateContributionPlanBundleDetailsMutation.async_mutate(
            self.user, id=self.deleted_details.id, json_ext={"changed": True})
        self.assertTrue(errors)
        self.assertNotIn(
            "changed", ContributionPlanBundleDetails.objects.get(id=self.deleted_details.id).json_ext or {})
