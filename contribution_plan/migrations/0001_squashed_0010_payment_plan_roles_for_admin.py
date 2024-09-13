# Generated by Django 3.2.15 on 2022-12-12 16:00

import contribution_plan.mixins
import core.fields
import datetime
import dirtyfields.dirtyfields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid

from core.utils import insert_role_right_for_system


def add_rights(apps, schema_editor):
    insert_role_right_for_system(64, 151101, apps)  # Contribution plan and bundle
    insert_role_right_for_system(64, 151102, apps)  # update
    insert_role_right_for_system(64, 151103, apps)  # delete
    insert_role_right_for_system(64, 151104, apps)  # update
    insert_role_right_for_system(64, 151106, apps)  # update
    insert_role_right_for_system(64, 151201, apps)  # Contribution plan
    insert_role_right_for_system(64, 151202, apps)  # Contribution plan
    insert_role_right_for_system(64, 151203, apps)  # Contribution plan
    insert_role_right_for_system(64, 151204, apps)  # Contribution plan
    insert_role_right_for_system(64, 151206, apps)  # Contribution plan
    insert_role_right_for_system(64, 157101, apps)  # Payment plan
    insert_role_right_for_system(64, 157102, apps)
    insert_role_right_for_system(64, 157103, apps)
    insert_role_right_for_system(64, 157104, apps)
    insert_role_right_for_system(64, 157106, apps)


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# contribution_plan.migrations.0009_contributionplan_roles_for_admin
# contribution_plan.migrations.0010_payment_plan_roles_for_admin

class Migration(migrations.Migration):

    replaces = [('contribution_plan', '0001_initial'), ('contribution_plan', '0002_auto_20201204_1353'), ('contribution_plan', '0003_auto_20201204_1439'), ('contribution_plan', '0004_auto_20201217_0946'), ('contribution_plan', '0005_contributionplanbundlemutation_contributionplanmutation'), ('contribution_plan', '0006_auto_20210118_1349'), ('contribution_plan', '0007_auto_20210217_1302'), ('contribution_plan', '0008_historicalpaymentplan_paymentplan'), ('contribution_plan', '0009_contributionplan_roles_for_admin'), ('contribution_plan', '0010_payment_plan_roles_for_admin')]

    initial = True

    dependencies = [
        ('core', '0015_missing_roles'),
        ('product', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calculation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributionPlan',
            fields=[
                ('id', models.UUIDField(db_column='UUID', default=None, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', null=True)),
                ('version', models.IntegerField(default=1)),
                ('date_valid_from', core.fields.DateTimeField(db_column='DateValidFrom', default=datetime.datetime.now)),
                ('date_valid_to', core.fields.DateTimeField(blank=True, db_column='DateValidTo', null=True)),
                ('replacement_uuid', models.UUIDField(db_column='ReplacementUUID', null=True)),
                ('code', models.CharField(blank=True, db_column='Code', max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('periodicity', models.IntegerField(db_column='Periodicity')),
                ('benefit_plan', models.ForeignKey(db_column='BenefitPlanID', on_delete=django.db.models.deletion.DO_NOTHING, to='product.product')),
                ('user_created', models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='contributionplan_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='contributionplan_user_updated', to=settings.AUTH_USER_MODEL)),
                ('calculation', models.UUIDField(db_column='calculationUUID')),
            ],
            options={
                'db_table': 'tblContributionPlan',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContributionPlanBundle',
            fields=[
                ('id', models.UUIDField(db_column='UUID', default=None, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', null=True)),
                ('version', models.IntegerField(default=1)),
                ('date_valid_from', core.fields.DateTimeField(db_column='DateValidFrom', default=datetime.datetime.now)),
                ('date_valid_to', core.fields.DateTimeField(blank=True, db_column='DateValidTo', null=True)),
                ('replacement_uuid', models.UUIDField(db_column='ReplacementUUID', null=True)),
                ('code', models.CharField(db_column='Code', max_length=255)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('user_created', models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='contributionplanbundle_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='contributionplanbundle_user_updated', to=settings.AUTH_USER_MODEL)),
                ('periodicity', models.IntegerField(blank=True, db_column='Periodicity', null=True)),
            ],
            options={
                'db_table': 'tblContributionPlanBundle',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ContributionPlanMutation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contribution_plan', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='mutations', to='contribution_plan.contributionplan')),
                ('mutation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contribution_plan', to='core.mutationlog')),
            ],
            options={
                'db_table': 'contribution_plan_ContributionPlanMutation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ContributionPlanBundleMutation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contribution_plan_bundle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='mutations', to='contribution_plan.contributionplanbundle')),
                ('mutation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contribution_plan_bundle', to='core.mutationlog')),
            ],
            options={
                'db_table': 'contribution_plan_bundle_ContributionPlanBundleMutation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ContributionPlanBundleDetails',
            fields=[
                ('id', models.UUIDField(db_column='UUID', default=None, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', null=True)),
                ('version', models.IntegerField(default=1)),
                ('date_valid_from', core.fields.DateTimeField(db_column='DateValidFrom', default=datetime.datetime.now)),
                ('date_valid_to', core.fields.DateTimeField(blank=True, db_column='DateValidTo', null=True)),
                ('replacement_uuid', models.UUIDField(db_column='ReplacementUUID', null=True)),
                ('contribution_plan', models.ForeignKey(db_column='ContributionPlanUUID', on_delete=django.db.models.deletion.DO_NOTHING, to='contribution_plan.contributionplan')),
                ('contribution_plan_bundle', models.ForeignKey(db_column='ContributionPlanBundleUUID', on_delete=django.db.models.deletion.DO_NOTHING, to='contribution_plan.contributionplanbundle')),
                ('user_created', models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='contributionplanbundledetails_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='contributionplanbundledetails_user_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tblContributionPlanBundleDetails',
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalContributionPlanBundle',
            fields=[
                ('id', models.UUIDField(db_column='UUID', db_index=True, default=None, editable=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', null=True)),
                ('version', models.IntegerField(default=1)),
                ('date_valid_from', core.fields.DateTimeField(db_column='DateValidFrom', default=datetime.datetime.now)),
                ('date_valid_to', core.fields.DateTimeField(blank=True, db_column='DateValidTo', null=True)),
                ('replacement_uuid', models.UUIDField(db_column='ReplacementUUID', null=True)),
                ('code', models.CharField(db_column='Code', max_length=255)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(blank=True, db_column='UserCreatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, db_column='UserUpdatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('periodicity', models.IntegerField(blank=True, db_column='Periodicity', null=True)),
            ],
            options={
                'verbose_name': 'historical contribution plan bundle',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalContributionPlanBundleDetails',
            fields=[
                ('id', models.UUIDField(db_column='UUID', db_index=True, default=None, editable=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', null=True)),
                ('version', models.IntegerField(default=1)),
                ('date_valid_from', core.fields.DateTimeField(db_column='DateValidFrom', default=datetime.datetime.now)),
                ('date_valid_to', core.fields.DateTimeField(blank=True, db_column='DateValidTo', null=True)),
                ('replacement_uuid', models.UUIDField(db_column='ReplacementUUID', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('contribution_plan', models.ForeignKey(blank=True, db_column='ContributionPlanUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contribution_plan.contributionplan')),
                ('contribution_plan_bundle', models.ForeignKey(blank=True, db_column='ContributionPlanBundleUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contribution_plan.contributionplanbundle')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(blank=True, db_column='UserCreatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, db_column='UserUpdatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical contribution plan bundle details',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalContributionPlan',
            fields=[
                ('id', models.UUIDField(db_column='UUID', db_index=True, default=None, editable=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', null=True)),
                ('version', models.IntegerField(default=1)),
                ('date_valid_from', core.fields.DateTimeField(db_column='DateValidFrom', default=datetime.datetime.now)),
                ('date_valid_to', core.fields.DateTimeField(blank=True, db_column='DateValidTo', null=True)),
                ('replacement_uuid', models.UUIDField(db_column='ReplacementUUID', null=True)),
                ('code', models.CharField(blank=True, db_column='Code', max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('periodicity', models.IntegerField(db_column='Periodicity')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('benefit_plan', models.ForeignKey(blank=True, db_column='BenefitPlanID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='product.product')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(blank=True, db_column='UserCreatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, db_column='UserUpdatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('calculation', models.UUIDField(db_column='calculationUUID', default='0e1b6dd4-04a0-4ee6-ac47-2a99cfa5e9a8')),
            ],
            options={
                'verbose_name': 'historical contribution plan',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='PaymentPlan',
            fields=[
                ('id', models.UUIDField(db_column='UUID', default=None, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', null=True)),
                ('version', models.IntegerField(default=1)),
                ('date_valid_from', core.fields.DateTimeField(db_column='DateValidFrom', default=datetime.datetime.now)),
                ('date_valid_to', core.fields.DateTimeField(blank=True, db_column='DateValidTo', null=True)),
                ('replacement_uuid', models.UUIDField(db_column='ReplacementUUID', null=True)),
                ('code', models.CharField(blank=True, db_column='Code', max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('calculation', models.UUIDField(db_column='calculationUUID')),
                ('periodicity', models.IntegerField(db_column='Periodicity')),
                ('benefit_plan', models.ForeignKey(db_column='BenefitPlanID', on_delete=django.db.models.deletion.DO_NOTHING, to='product.product')),
                ('user_created', models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='paymentplan_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='paymentplan_user_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tblPaymentPlan',
            },
            bases=(contribution_plan.mixins.GenericPlanQuerysetMixin, dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPaymentPlan',
            fields=[
                ('id', models.UUIDField(db_column='UUID', db_index=True, default=None, editable=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', null=True)),
                ('version', models.IntegerField(default=1)),
                ('date_valid_from', core.fields.DateTimeField(db_column='DateValidFrom', default=datetime.datetime.now)),
                ('date_valid_to', core.fields.DateTimeField(blank=True, db_column='DateValidTo', null=True)),
                ('replacement_uuid', models.UUIDField(db_column='ReplacementUUID', null=True)),
                ('code', models.CharField(blank=True, db_column='Code', max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('calculation', models.UUIDField(db_column='calculationUUID')),
                ('periodicity', models.IntegerField(db_column='Periodicity')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('benefit_plan', models.ForeignKey(blank=True, db_column='BenefitPlanID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='product.product')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(blank=True, db_column='UserCreatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, db_column='UserUpdatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical payment plan',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.RunPython(
            code=add_rights,
        ),
    ]
