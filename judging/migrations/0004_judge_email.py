# Generated by Django 2.2.1 on 2019-05-28 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judging', '0003_auto_20190527_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge',
            name='email',
            field=models.EmailField(default='test@email.com', max_length=254),
            preserve_default=False,
        ),
    ]
