# Generated by Django 2.2.19 on 2022-03-26 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(auto_now=True)),
                ('btc_address', models.CharField(blank=True, max_length=150, null=True)),
                ('amount_to_pay', models.CharField(blank=True, choices=[('Full Amount', 'Full Amount'), ('Specific Amount', 'Specific Amount')], max_length=15, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Done', 'Done')], default='Pending', max_length=11, null=True)),
                ('payment_method', models.CharField(blank=True, choices=[('BTC', 'BTC')], default='BTC', max_length=10, null=True)),
                ('actual_amount', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payout_user', to=settings.AUTH_USER_MODEL, verbose_name='payout_user')),
            ],
        ),
    ]
