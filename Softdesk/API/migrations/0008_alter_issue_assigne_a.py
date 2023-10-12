# Generated by Django 4.2.5 on 2023-10-05 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_project_contributors_alter_user_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assigne_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues_assignees', to='API.contributor'),
        ),
    ]
