# Generated by Django 5.0 on 2024-01-22 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='account/media/uploads/user.png', null=True, upload_to='account/media/uploads/'),
        ),
    ]
