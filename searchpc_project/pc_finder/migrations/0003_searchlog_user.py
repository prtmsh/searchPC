# Generated by Django 5.0.1

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pc_finder', '0002_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchlog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='searches', to=settings.AUTH_USER_MODEL),
        ),
    ]
