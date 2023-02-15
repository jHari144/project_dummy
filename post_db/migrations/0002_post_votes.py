# Generated by Django 4.1.6 on 2023-02-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post_db", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post_votes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("post_id", models.IntegerField(default=0)),
                ("user_id", models.IntegerField(default=0)),
                ("up_or_d", models.IntegerField(default=0)),
            ],
        ),
    ]
