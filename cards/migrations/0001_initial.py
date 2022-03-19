# Generated by Django 4.0.2 on 2022-02-28 20:16

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
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=35, null=True, unique=True)),
                ('status', models.CharField(blank=True, choices=[('Stop', 'Stop'), ('Working', 'Working')], default='Working', max_length=11, null=True)),
            ],
            options={
                'verbose_name': 'Batch',
                'verbose_name_plural': 'Batch',
                'db_table': 'Batch',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=6, null=True)),
                ('name', models.CharField(blank=True, max_length=35, null=True)),
            ],
            options={
                'verbose_name': 'Country Codes',
                'verbose_name_plural': 'Country Codes',
                'db_table': 'Country And Codes',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CouponCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('cvv', models.CharField(blank=True, max_length=6, null=True)),
                ('sold', models.BooleanField(default=False)),
                ('in_my_cart', models.BooleanField(blank=True, default=False, null=True)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_batch', to='cards.batch')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Coupon Card',
                'verbose_name_plural': 'Coupon Card',
                'db_table': 'Coupon Card',
                'abstract': False,
            },
        ),
    ]