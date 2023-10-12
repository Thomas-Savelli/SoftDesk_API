from django.contrib import admin
from API.models import (User,
                        Project,
                        Issue,
                        Comment)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'can_be_contacted',
                    'can_data_be_shared', 'date_of_birth')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_created',
                    'type', 'creator')


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',
                    'creator', 'assigne_a',
                    'statut', 'priority',
                    'balise')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('issue', 'creator',
                    'texte', 'link_issue')
