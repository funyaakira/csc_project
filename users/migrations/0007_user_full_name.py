# Generated by Django 2.1.2 on 2018-11-11 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='氏名'),
        ),
    ]
