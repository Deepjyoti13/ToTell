# Generated by Django 3.0.8 on 2020-07-25 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0015_remove_post_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_writer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.Writer'),
        ),
    ]
