# Generated by Django 4.0.3 on 2022-03-13 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '주문', 'verbose_name_plural': '주문'},
        ),
    ]
