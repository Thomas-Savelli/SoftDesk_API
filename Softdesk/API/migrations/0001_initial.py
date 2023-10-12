# Generated by Django 4.2.5 on 2023-10-02 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_be_contacted', models.BooleanField(default=False)),
                ('can_data_be_shared', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=2048)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('back-end', 'Back-end'), ('front-end', 'Front-end'), ('iOS', 'iOS'), ('Android', 'Android'), ('web', 'Web Development'), ('mobile', 'Mobile Development'), ('data', 'Data Science'), ('ai', 'Artificial Intelligence'), ('iot', 'Internet of Things')], max_length=20)),
                ('contributors', models.ManyToManyField(related_name='projects_contributed_to', to='API.contributor')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to='API.contributor')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('statut', models.CharField(choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Finished', 'Finished')], default='To Do', max_length=20)),
                ('priority', models.CharField(choices=[('LOW', 'LOW'), ('MEDIUM', 'MEDIUM'), ('HIGH', 'HIGH')], default='MEDIUM', max_length=10)),
                ('balise', models.CharField(choices=[('BUG', 'BUG'), ('FEATURE', 'FEATURE'), ('TASK', 'TASK')], default='TASK', max_length=10)),
                ('assigne_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues_assignees', to='API.contributor')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.contributor')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.project')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texte', models.TextField()),
                ('contributeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.contributor')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.issue')),
                ('link_issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linked_issue', to='API.issue')),
            ],
        ),
    ]
