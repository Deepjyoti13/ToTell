# Generated by Django 3.0.8 on 2020-07-25 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0011_auto_20200725_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.Writer'),
        ),
    ]