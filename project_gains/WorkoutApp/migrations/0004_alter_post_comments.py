# Generated by Django 4.1.2 on 2023-04-16 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WorkoutApp', '0003_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WorkoutApp.post'),
        ),
    ]
