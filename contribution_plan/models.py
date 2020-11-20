import uuid

from django.conf import settings
from django.db import models
from core import models as core_models, fields
from graphql import ResolveInfo
from jsonfallback.fields import FallbackJSONField
from product.models import Product


class ContributionPlanBundleManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(ContributionPlanBundleManager, self).filter(*args, **kwargs)


class ContributionPlanBundle(core_models.UUIDVersionedModel):
    id = models.AutoField(db_column='ContributionPlanBundleId', primary_key=True)
    uuid = models.CharField(db_column='ContributionPlanBundleUUID', max_length=36, default=uuid.uuid4, unique=True)
    version = models.IntegerField()

    active = models.BooleanField(db_column='Active')
    code = models.CharField(db_column='ContributionPlanBundleCode', max_length=255, blank=True, null=True)
    name = models.CharField(db_column='ContributionPlanBundleName', max_length=255, blank=True, null=True)

    json_ext = FallbackJSONField(db_column='Json_ext', blank=True, null=True)

    date_created = fields.DateTimeField(db_column="DateCreated")
    date_updated = fields.DateTimeField(db_column="DateUpdated", null=True)

    user_updated = models.ForeignKey(core_models.User, db_column="UserUpdatedUUID",
                                     related_name="%(class)s_UpdatedUUID", on_delete=models.deletion.DO_NOTHING,
                                     null=True)
    user_created = models.ForeignKey(core_models.User, db_column="UserCreatedUUID",
                                     related_name="%(class)s_CreatedUUID", on_delete=models.deletion.DO_NOTHING)

    date_valid_from = fields.DateTimeField(db_column="DateValidFrom")
    date_valid_to = fields.DateTimeField(db_column="DateValidTo", null=True)

    objects = ContributionPlanBundleManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=-1)
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


class ContributionPlan(core_models.UUIDVersionedModel):
    id = models.AutoField(db_column='ContributionPlanId', primary_key=True)
    uuid = models.CharField(db_column='ContributionPlanUUID', max_length=36, default=uuid.uuid4, unique=True)
    version = models.IntegerField()

    active = models.BooleanField(db_column='Active')

    code = models.CharField(db_column='ContributionPlanCode', max_length=255, blank=True, null=True)
    # calculation = models.ForeignKey(Calculation, db_column="CalculationUUID", on_delete=models.deletion.DO_NOTHING)
    benefit_plan = models.ForeignKey(Product, db_column="BenefitPlanUUID", on_delete=models.deletion.DO_NOTHING)
    periodicity = models.IntegerField()

    json_ext = FallbackJSONField(db_column='Json_ext', blank=True, null=True)

    date_created = fields.DateTimeField(db_column="DateCreated")
    amendment = models.IntegerField()
    date_updated = fields.DateTimeField(db_column="DateUpdated", null=True)

    user_updated = models.ForeignKey(core_models.User, db_column="UserUpdatedUUID", null=True,
                                     related_name="%(class)s_UpdatedUUID", on_delete=models.deletion.DO_NOTHING)
    user_created = models.ForeignKey(core_models.User, db_column="UserCreatedUUID",
                                     related_name="%(class)s_CreatedUUID", on_delete=models.deletion.DO_NOTHING)

    date_valid_from = fields.DateTimeField(db_column="DateValidFrom")
    date_valid_to = fields.DateTimeField(db_column="DateValidTo", null=True)

    objects = ContributionPlanManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=-1)
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


class ContributionPlanBundleDetails(core_models.UUIDVersionedModel):
    id = models.AutoField(db_column='ContributionPlanBundleDetailsId', primary_key=True)
    uuid = models.CharField(db_column='ContributionPlanBundleDetailsUUID', max_length=36,
                            default=uuid.uuid4, unique=True)
    version = models.IntegerField()

    contribution_plan_bundle = models.ForeignKey(ContributionPlanBundle, db_column="ContributionPlanBundleUUID",
                                                 on_delete=models.deletion.DO_NOTHING)

    contribution_plan = models.ForeignKey(ContributionPlan, db_column="ContributionPlanUUID",
                                          on_delete=models.deletion.DO_NOTHING)

    json_ext = FallbackJSONField(db_column='Json_ext', blank=True, null=True)

    date_created = fields.DateTimeField(db_column="DateCreated")
    date_updated = fields.DateTimeField(db_column="DateUpdated", null=True)

    user_updated = models.ForeignKey(core_models.User, db_column="UserUpdatedUUID", null=True,
                                     related_name="%(class)s_UpdatedUUID", on_delete=models.deletion.DO_NOTHING)
    user_created = models.ForeignKey(core_models.User, db_column="UserCreatedUUID",
                                     related_name="%(class)s_CreatedUUID", on_delete=models.deletion.DO_NOTHING)

    date_valid_from = fields.DateTimeField(db_column="DateValidFrom")
    date_valid_to = fields.DateTimeField(db_column="DateValidTo", null=True)

    active = models.BooleanField(db_column='Active')

    objects = ContributionPlanBundleDetailsManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=-1)
        if settings.ROW_SECURITY:
            pass
        return queryset

    class Meta:
        db_table = 'tblContributionPlanBundleDetails'
