# Generated by Django 4.2.5 on 2023-10-05 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_remove_project_contributors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.user'),
        ),
    ]