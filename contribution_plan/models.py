import uuid

from django.db import models
from core import models as core_models, fields
from jsonfallback.fields import FallbackJSONField
from product.models import Product


class ContributionPlanBundle(core_models.UUIDVersionedModel):
    id = models.AutoField(db_column='ContributionPlanBundleId', primary_key=True)
    uuid = models.CharField(db_column='ContributionPlanBundleUUID', max_length=24, default=uuid.uuid4, unique=True)
    version = models.IntegerField()

    active = models.BooleanField(db_column='Active')
    code = models.CharField(db_column='ContributionPlanBundleCode', max_length=255, blank=True, null=True)
    name = models.CharField(db_column='ContributionPlanBundleName', max_length=255, blank=True, null=True)

    json_ext = FallbackJSONField(db_column='Json_ext', blank=True, null=True)

    date_created = fields.DateTimeField(db_column="DateCreated")
    date_updated = fields.DateTimeField(db_column="DateUpdated")

    user_updated = models.ForeignKey(core_models.InteractiveUser, db_column="UserUpdatedUUID",
                                     related_name="%(class)s_UpdatedUUID", on_delete=models.deletion.DO_NOTHING)
    user_created = models.ForeignKey(core_models.InteractiveUser, db_column="UserCreatedUUID",
                                     related_name="%(class)s_CreatedUUID", on_delete=models.deletion.DO_NOTHING)

    date_valid_from = fields.DateTimeField(db_column="DateValidFrom")
    date_valid_to = fields.DateTimeField("DateValidTo")

    class Meta:
        db_table = 'tblContributionPlanBundle'


class ContributionPlan(core_models.UUIDVersionedModel):
    id = models.AutoField(db_column='ContributionPlanId', primary_key=True)
    uuid = models.CharField(db_column='ContributionPlanUUID', max_length=24, default=uuid.uuid4, unique=True)
    version = models.IntegerField()

    active = models.BooleanField(db_column='Active')

    code = models.CharField(db_column='ContributionPlanCode', max_length=255, blank=True, null=True)
    # calculation = models.ForeignKey(Calculation, db_column="CalculationUUID", on_delete=models.deletion.DO_NOTHING)
    benefit_plan = models.ForeignKey(Product, db_column="BenefitPlanUUID", on_delete=models.deletion.DO_NOTHING)
    periodicity = models.IntegerField()

    json_ext = FallbackJSONField(db_column='Json_ext', blank=True, null=True)

    date_created = fields.DateTimeField(db_column="DateCreated")
    amendment = models.IntegerField()
    date_updated = fields.DateTimeField(db_column="DateUpdated")

    user_updated = models.ForeignKey(core_models.InteractiveUser, db_column="UserUpdatedUUID",
                                     related_name="%(class)s_UpdatedUUID", on_delete=models.deletion.DO_NOTHING)
    user_created = models.ForeignKey(core_models.InteractiveUser, db_column="UserCreatedUUID",
                                     related_name="%(class)s_CreatedUUID", on_delete=models.deletion.DO_NOTHING)

    date_valid_from = fields.DateTimeField(db_column="DateValidFrom")
    date_valid_to = fields.DateTimeField("DateValidTo")

    class Meta:
        db_table = 'tblContributionPlan'


class ContributionPlanBundleDetailsManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(ContributionPlanBundleDetailsManager, self).filter(*args, **kwargs)


class ContributionPlanBundleDetails(models.Model):
    id = models.AutoField(db_column='ContributionPlanBundleDetailsId', primary_key=True)
    uuid = models.CharField(db_column='ContributionPlanBundleDetailsUUID',
                            max_length=24, default=uuid.uuid4, unique=True)
    version = models.IntegerField()

    contribution_plan_bundle = models.ForeignKey(ContributionPlanBundle, db_column="ContributionPlanBundleUUID",
                                                 on_delete=models.deletion.DO_NOTHING)

    contribution_plan = models.ForeignKey(ContributionPlan, db_column="ContributionPlanUUID",
                                          on_delete=models.deletion.DO_NOTHING)

    json_ext = FallbackJSONField(db_column='Json_ext', blank=True, null=True)

    date_created = fields.DateTimeField(db_column="DateCreated")
    date_updated = fields.DateTimeField(db_column="DateUpdated")

    user_updated = models.ForeignKey(core_models.InteractiveUser, db_column="UserUpdatedUUID",
                                     related_name="%(class)s_UpdatedUUID", on_delete=models.deletion.DO_NOTHING)
    user_created = models.ForeignKey(core_models.InteractiveUser, db_column="UserCreatedUUID",
                                     related_name="%(class)s_CreatedUUID", on_delete=models.deletion.DO_NOTHING)

    date_valid_from = fields.DateTimeField(db_column="DateValidFrom")
    date_valid_to = fields.DateTimeField("DateValidTo")

    active = models.BooleanField(db_column='Active')

    object = ContributionPlanBundleDetailsManager()

    class Meta:
        db_table = 'tblContributionPlanBundleDetails'
