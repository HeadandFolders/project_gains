# Generated by Django 4.1.2 on 2023-04-18 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkoutApp', '0004_alter_post_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, null=True, related_name='PostCom', to='WorkoutApp.post'),
        ),
    ]