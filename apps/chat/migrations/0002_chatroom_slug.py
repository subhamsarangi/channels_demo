# Generated by Django 5.1.3 on 2024-12-03 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
    ]