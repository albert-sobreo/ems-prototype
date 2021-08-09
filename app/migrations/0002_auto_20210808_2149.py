# Generated by Django 3.2.3 on 2021-08-08 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dtr',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dtr',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dtr', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='dateTimeIn',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='dateTimeOut',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]