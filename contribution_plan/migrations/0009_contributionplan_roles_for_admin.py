import logging

from django.db import migrations

from core.utils import insert_role_right_for_system

logger = logging.getLogger(__name__)


def add_rights(apps, schema_editor):
    insert_role_right_for_system(64, 151101)  # Contribution plan and bundle
    insert_role_right_for_system(64, 153002)  # update
    insert_role_right_for_system(64, 153003)  # delete
    insert_role_right_for_system(64, 153004)  # update
    insert_role_right_for_system(64, 153006)  # update
    insert_role_right_for_system(64, 151201)  # Contribution plan
    insert_role_right_for_system(64, 151202)  # Contribution plan
    insert_role_right_for_system(64, 151203)  # Contribution plan
    insert_role_right_for_system(64, 151204)  # Contribution plan
    insert_role_right_for_system(64, 151206)  # Contribution plan


class Migration(migrations.Migration):
    dependencies = [
        ('contribution_plan', '0008_historicalpaymentplan_paymentplan')
    ]

    operations = [
        migrations.RunPython(add_rights),
    ]
