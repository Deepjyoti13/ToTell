# Generated by Django 3.0.7 on 2020-11-20 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0014_post_declined'),
    ]

    operations = [
        migrations.AddField(
            model_name='writer',
            name='designation',
            field=models.CharField(blank=True, default='Writer', max_length=20, null=True),
        ),
    ]
