# Generated by Django 4.1.2 on 2023-04-22 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkoutApp', '0010_alter_userprofile_banner_pic_alter_userprofile_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='saved_posts',
            field=models.ManyToManyField(to='WorkoutApp.post'),
        ),
    ]
