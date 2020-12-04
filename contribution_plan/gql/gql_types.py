import graphene
from contribution_plan.models import ContributionPlanBundle, ContributionPlan, ContributionPlanBundleDetails
from core import ExtendedConnection, prefix_filterset
from graphene_django import DjangoObjectType


class ContributionPlanBundleGQLType(DjangoObjectType):

    class Meta:
        model = ContributionPlanBundle
        exclude_fields = ('row_id',)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            #"uuid": ["exact"],
            "version": ["exact"],
            #"active": ["exact"],
            "code": ["exact"],
            "name": ["exact"],
            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "user_created": ["exact"],
            "user_updated": ["exact"],
            "date_valid_from": ["exact", "lt", "lte", "gt", "gte"],
            "date_valid_to": ["exact", "lt", "lte", "gt", "gte"],
        }

        connection_class = ExtendedConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return ContributionPlanBundle.get_queryset(queryset, info)


class ContributionPlanGQLType(DjangoObjectType):

    class Meta:
        model = ContributionPlan
        exclude_fields = ('row_id',)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            #"uuid": ["exact"],
            "version": ["exact"],
            #"active": ["exact"],
            "code": ["exact"],
            "benefit_plan": ["exact"],
            "periodicity": ["exact", "lt", "lte", "gt", "gte"],
            #"amendment": ["exact", "lt", "lte", "gt", "gte"],
            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "user_created": ["exact"],
            "user_updated": ["exact"],
            "date_valid_from": ["exact", "lt", "lte", "gt", "gte"],
            "date_valid_to": ["exact", "lt", "lte", "gt", "gte"],
        }

        connection_class = ExtendedConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return ContributionPlan.get_queryset(queryset, info)


class ContributionPlanBundleDetailsGQLType(DjangoObjectType):

    class Meta:
        model = ContributionPlanBundleDetails
        exclude_fields = ('row_id',)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            #"uuid": ["exact"],
            "version": ["exact"],
            **prefix_filterset("contribution_plan_bundle__",
                               ContributionPlanBundleGQLType._meta.filter_fields),
            **prefix_filterset("contribution_plan__",
                               ContributionPlanGQLType._meta.filter_fields),
            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "user_created": ["exact"],
            "user_updated": ["exact"],
            "date_valid_from": ["exact", "lt", "lte", "gt", "gte"],
            "date_valid_to": ["exact", "lt", "lte", "gt", "gte"],
            #"active": ["exact"]
        }

        connection_class = ExtendedConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return ContributionPlanBundleDetails.get_queryset(queryset, info)

