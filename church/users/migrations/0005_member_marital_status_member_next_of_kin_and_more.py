# Generated by Django 4.1.9 on 2023-07-20 11:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="marital_status",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="member",
            name="next_of_kin",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="member",
            name="occupation",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="group",
            name="members",
            field=models.ManyToManyField(related_name="groups", to="users.member"),
        ),
    ]
