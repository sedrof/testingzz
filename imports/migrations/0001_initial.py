# Generated by Django 4.0.2 on 2022-02-28 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(blank=True, max_length=50, null=True)),
                ('countr_name', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Import',
                'verbose_name_plural': 'Import',
            },
        ),
    ]
