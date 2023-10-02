from django.contrib.auth.models import User
from django.db import models

from django.core.exceptions import ValidationError
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=False)

    def clean(self):
        # Vérifiez que l'utilisateur a plus de 15 ans
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month,
                                                                                  self.date_of_birth.day))
        if age < 15:
            raise ValidationError("L'utilisateur doit avoir plus de 15 ans.")


class Contributor(models.Model):
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)


class Project(models.Model):
    TYPE_CHOICES = (
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('data', 'Data Science'),
        ('ai', 'Artificial Intelligence'),
        ('iot', 'Internet of Things'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    date_created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    creator = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(Contributor)


class Issue(models.Model):
    STATUT_CHOICES = (
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished'),
    )
    PRIORITE_CHOICES = (
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH'),
    )
    BALISE_CHOICES = (
        ('BUG', 'BUG'),
        ('FEATURE', 'FEATURE'),
        ('TASK', 'TASK'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    creator = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    assigne_a = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='issues_assignees')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='To Do')
    priority = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='MEDIUM')
    balise = models.CharField(max_length=10, choices=BALISE_CHOICES, default='TASK')


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    contributeur = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    texte = models.TextField()
    link_issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='linked_issue')
