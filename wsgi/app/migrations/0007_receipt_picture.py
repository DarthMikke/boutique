# Generated by Django 5.0.3 on 2024-06-25 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_productsize_purchase_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
