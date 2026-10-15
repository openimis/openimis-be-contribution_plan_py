from django.conf import settings
from django.db import models
from graphql import ResolveInfo

from core.models import HistoryModelManager


class GenericPlanManager(HistoryModelManager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(GenericPlanManager, self).filter(*args, **kwargs)


class GenericPlanQuerysetMixin:
    """Row security only.

    Soft-delete scoping deliberately does not happen here. get_queryset is
    handed the queryset and the user, never the filter arguments, so it cannot
    tell whether the caller asked for deleted rows - and a queryset already
    narrowed to is_deleted=False cannot be widened again by a filter. Forcing
    it here is what made "show deleted" resolve to is_deleted=True AND
    is_deleted=False, an empty list for every row (OP-3180).

    The default now comes from append_validity_filter(), which the resolvers
    call and which does see the arguments.
    """

    @classmethod
    def get_queryset(cls, queryset, user):
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=-1)
        if settings.ROW_SECURITY:
            pass
        return queryset
