# Generated by Django 4.1.4 on 2022-12-24 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_partner_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
