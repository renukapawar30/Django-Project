# Generated by Django 3.2.8 on 2022-02-27 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='location',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]