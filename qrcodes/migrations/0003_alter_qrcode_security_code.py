# Generated by Django 5.0.6 on 2024-06-13 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrcodes', '0002_remove_qrcode_code_remove_qrcode_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='security_code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
