# Generated by Django 3.1 on 2022-05-31 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_auto_20220525_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photo.post'),
        ),
    ]
