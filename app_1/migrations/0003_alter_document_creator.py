# Generated by Django 4.2.1 on 2023-09-11 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='creator',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]
