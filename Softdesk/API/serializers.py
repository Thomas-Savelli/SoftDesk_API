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
        fields = ['username', 'email',
                  'date_of_birth', 'can_be_contacted',
                  'can_data_be_shared']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'date_of_birth', 'can_be_contacted',
                  'can_data_be_shared']


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
        fields = ['id', 'creator', 'date_created', 'texte']


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'name', 'description',
                  'creator', 'date_created', 'assigne_a', 'statut',
                  'priority', 'balise']


class IssueSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='creator.username', read_only=True)
    # comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description',
                  'creator', 'date_created', 'assigne_a', 'statut',
                  'priority', 'balise']

    def get_creator(self, instance):
        return instance.creator.username

    # def get_comments(self, instance):
    #     comments = Comment.objects.filter(issue=instance)
    #     serialized_comments = []

    #     for comment in comments:
    #         serialized_comment = {
    #             'id': comment.id,
    #             'creator': comment.creator.contributor.username,
    #             'date_created': comment.date_created,
    #             'texte': comment.texte,
    #         }
    #         serialized_comments.append(serialized_comment)
    #     return serialized_comments


class ProjectDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'creator',
                  'date_created', 'description',
                  'contributors']

    def get_creator(self, instance):
        return instance.creator.username

    def get_contributors(self, instance):
        contributors = Contributor.objects.filter(project=instance)
        return [contributor.contributor.username for contributor in contributors]


class ProjectSerializer(serializers.ModelSerializer):
    # To create new Project
    class Meta:
        model = Project
        fields = ['name', 'description', 'type']
