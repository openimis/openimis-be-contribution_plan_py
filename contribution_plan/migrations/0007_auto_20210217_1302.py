# Generated by Django 3.0.3 on 2021-02-17 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribution_plan', '0006_auto_20210118_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributionplan',
            name='calculation',
            field=models.UUIDField(db_column='calculationUUID'),
        ),
        migrations.AlterField(
            model_name='historicalcontributionplan',
            name='calculation',
            field=models.UUIDField(db_column='calculationUUID', default='0e1b6dd4-04a0-4ee6-ac47-2a99cfa5e9a8'),
            preserve_default=False,
        ),
    ]