# Generated by Django 4.0.3 on 2022-03-13 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': '상품', 'verbose_name_plural': '상품'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='stuck',
            new_name='stock',
        ),
        migrations.AlterModelTable(
            name='product',
            table='fastcampus_product',
        ),
    ]
