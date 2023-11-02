from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import (User,
                     Contributor,
                     Project,
                     Issue,
                     Comment)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'date_of_birth', 'can_be_contacted',
                  'can_data_be_shared']


class ContributorSerializer(serializers.ModelSerializer):
    contributor = UserSerializer(source='contributor.contributor', read_only=True)

    class Meta:
        model = Contributor
        fields = ['contributor', 'project']


class ProjectListSerializer(ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'type',
                  'date_created', 'description',
                  'creator']

    def get_creator(self, instance):
        return instance.creator.username


class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'creator', 'texte']

    


class IssueSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='creator.username', read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description',
                  'creator', 'assigne_a', 'statut',
                  'priority', 'balise', 'comments']

    def get_creator(self, instance):
        return instance.creator.username

    def get_comments(self, instance):
        comments = Comment.objects.filter(issue=instance)
        serialized_comments = []

        for comment in comments:
            serialized_comment = {
                'id': comment.id,
                'creator': comment.creator.contributor.username,
                'texte': comment.texte,
            }
            serialized_comments.append(serialized_comment)
        return serialized_comments


class ProjectDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'creator',
                  'date_created', 'description',
                  'contributors', 'issues']

    def get_creator(self, instance):
        return instance.creator.username

    def get_contributors(self, instance):
        contributors = Contributor.objects.filter(project=instance)
        return [contributor.contributor.username for contributor in contributors]

    def get_issues(self, instance):
        issues = Issue.objects.filter(project=instance)
        serialized_issues = []

        for issue in issues:
            serialized_issue = {
                'id': issue.id,
                'name': issue.name,
                'priority': issue.priority,
                'description': issue.description,
                'creator': issue.creator.username,
                'baslise': issue.balise,
                'status': issue.statut,
                'assigne-to': issue.assigne_a
            }
            serialized_issues.append(serialized_issue)
        return serialized_issues


class ProjectSerializer(serializers.ModelSerializer):
    # To create new Project
    class Meta:
        model = Project
        fields = ['name', 'description', 'type']
