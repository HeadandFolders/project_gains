# Generated by Django 4.1.2 on 2023-04-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkoutApp', '0008_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='banner_pic',
            field=models.ImageField(blank=True, default='media/WorkoutApp/banners/yes6.jpg', null=True, upload_to='media/WorkoutApp/banners', verbose_name='banner pic'),
        ),
    ]
