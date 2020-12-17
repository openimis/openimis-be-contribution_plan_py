from django.conf import settings
from django.db import models
from core import models as core_models, fields
from graphql import ResolveInfo
from product.models import Product
from calculation.models import CalculationRules


class ContributionPlanBundleManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(ContributionPlanBundleManager, self).filter(*args, **kwargs)


class ContributionPlanBundle(core_models.HistoryBusinessModel):
    code = models.CharField(db_column='Code', max_length=255, null=False)
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)
    periodicity = models.IntegerField(db_column="Periodicity", blank=True, null=True)

    objects = ContributionPlanBundleManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=None)
        if settings.ROW_SECURITY:
            pass
        return queryset

    class Meta:
        db_table = 'tblContributionPlanBundle'


class ContributionPlanManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(ContributionPlanManager, self).filter(*args, **kwargs)


class ContributionPlan(core_models.HistoryBusinessModel):
    code = models.CharField(db_column="Code", max_length=255, blank=True, null=True)
    name = models.CharField(db_column="Name", max_length=255, blank=True, null=True)
    calculation = models.ForeignKey(CalculationRules, db_column="CalculationUUID", on_delete=models.deletion.DO_NOTHING)
    benefit_plan = models.ForeignKey(Product, db_column="BenefitPlanID", on_delete=models.deletion.DO_NOTHING)
    periodicity = models.IntegerField(db_column="Periodicity", null=False)

    objects = ContributionPlanManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=None)
        if settings.ROW_SECURITY:
            pass
        return queryset

    class Meta:
        db_table = 'tblContributionPlan'


class ContributionPlanBundleDetailsManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(ContributionPlanBundleDetailsManager, self).filter(*args, **kwargs)


class ContributionPlanBundleDetails(core_models.HistoryBusinessModel):
    contribution_plan_bundle = models.ForeignKey(ContributionPlanBundle, db_column="ContributionPlanBundleUUID",
                                                 on_delete=models.deletion.DO_NOTHING)
    contribution_plan = models.ForeignKey(ContributionPlan, db_column="ContributionPlanUUID",
                                          on_delete=models.deletion.DO_NOTHING)

    objects = ContributionPlanBundleDetailsManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=None)
        if settings.ROW_SECURITY:
            pass
        return queryset

    class Meta:
        db_table = 'tblContributionPlanBundleDetails'