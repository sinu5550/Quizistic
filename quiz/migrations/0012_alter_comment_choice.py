# Generated by Django 5.0 on 2024-01-20 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_alter_comment_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='choice',
            field=models.IntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')]),
        ),
    ]
