# Generated by Django 4.1.4 on 2022-12-26 10:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_client_address_client_phone_alter_partner_lstate'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='client',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='cards.client'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='agent',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.client'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
