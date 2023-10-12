# Generated by Django 4.2.5 on 2023-10-05 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_alter_issue_assigne_a'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='contributeur',
            new_name='creator',
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='API.project'),
            preserve_default=False,
        ),
    ]