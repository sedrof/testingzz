# Generated by Django 2.2.19 on 2022-03-26 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('address', models.CharField(blank=True, max_length=25, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
