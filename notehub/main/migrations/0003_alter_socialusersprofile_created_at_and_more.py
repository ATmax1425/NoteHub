# Generated by Django 5.0.6 on 2024-07-15 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_socialusersprofile_alter_userprofile_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialusersprofile',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='socialusersprofile',
            name='updated_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]
