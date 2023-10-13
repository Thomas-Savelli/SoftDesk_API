from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import (User,
                     Contributor,
                     Project,
                     Issue)


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
    contributor = UserSerializer()

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


class IssueSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True,
                                                 default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description',
                  'creator', 'assigne_a', 'statut',
                  'priority', 'balise']


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
