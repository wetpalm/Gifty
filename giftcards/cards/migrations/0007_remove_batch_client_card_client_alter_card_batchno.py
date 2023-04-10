# Generated by Django 4.1.4 on 2022-12-26 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_remove_card_client_alter_batch_client_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='client',
        ),
        migrations.AddField(
            model_name='card',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='batchno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.batch'),
        ),
    ]