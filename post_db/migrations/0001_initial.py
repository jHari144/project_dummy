# Generated by Django 4.1.6 on 2023-02-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Posts",
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
                ("post_title", models.CharField(max_length=100)),
                ("post_text", models.CharField(max_length=800)),
                ("pub_date", models.DateTimeField(verbose_name="date published")),
                ("score", models.IntegerField(default=0)),
                ("views", models.IntegerField(default=0)),
            ],
        ),
    ]