# Generated by Django 4.1.6 on 2023-02-15 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post_db", "0003_replies"),
    ]

    operations = [
        migrations.AddField(
            model_name="posts",
            name="no_replies",
            field=models.IntegerField(default=0),
        ),
    ]
