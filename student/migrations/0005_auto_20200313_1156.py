# Generated by Django 2.1 on 2020-03-13 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20200313_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='level',
        ),
        migrations.RemoveField(
            model_name='student',
            name='studentclass',
        ),
        migrations.AddField(
            model_name='student',
            name='level_id',
            field=models.IntegerField(blank=0, default=1),
            preserve_default=False,
        ),
    ]
