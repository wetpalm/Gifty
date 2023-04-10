# Generated by Django 4.1.4 on 2022-12-26 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_remove_batch_client_card_client_alter_card_batchno'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='status',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='batch',
            name='amount',
            field=models.IntegerField(default=5000),
        ),
        migrations.AlterField(
            model_name='batch',
            name='batchno',
            field=models.CharField(max_length=5, unique=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='cardno',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
