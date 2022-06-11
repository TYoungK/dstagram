# Generated by Django 3.1 on 2022-05-25 04:45

import accounts.models
import config.asset_storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20220525_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='profile_pic/base/empty_user_icon.png', storage=config.asset_storage.ProfileStorage(), upload_to=accounts.models.User.profile_pic_upload),
        ),
    ]
