"""get_queryset honours the OP-2029 validity contract (epic OP-3317, phase 1).

Explicit validity values return the expected rows; a caller asking for
nothing gets what it got before the contract existed.
"""

from datetime import timedelta

from django.test import TestCase

from core.models.row_filters import Validity
from core.test_helpers import assert_row_filters, create_test_interactive_user, mark_deleted
from contribution_plan.models import ContributionPlanBundle
from contribution_plan.tests.helpers import create_test_contribution_plan_bundle


class ContributionPlanBundleRowFiltersTest(TestCase):
    def test_bundle(self):
        user = create_test_interactive_user(username="cpbrowfilters")
        live = create_test_contribution_plan_bundle(custom_props={"code": "RWF1"})
        deleted = mark_deleted(create_test_contribution_plan_bundle(custom_props={"code": "RWF2"}))
        assert_row_filters(
            self, ContributionPlanBundle,
            ContributionPlanBundle.objects.filter(id__in=[live.id, deleted.id]), user,
            live.id, deleted.id, default_hides_deleted=False,
        )

    def test_a_validity_date_uses_the_business_dates(self):
        user = create_test_interactive_user(username="cpbrowfilters")
        bundle = create_test_contribution_plan_bundle(custom_props={"code": "RWF3"})
        rows = ContributionPlanBundle.objects.filter(id=bundle.id)
        before = bundle.date_valid_from - timedelta(days=1)
        self.assertFalse(ContributionPlanBundle.get_queryset(rows, user, validity=Validity.at(before)).exists())
        self.assertTrue(
            ContributionPlanBundle.get_queryset(rows, user, validity=Validity.at(bundle.date_valid_from)).exists()
        )
