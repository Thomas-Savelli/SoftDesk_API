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

    class Meta:
        model = Issue
        fields = ['id', 'name', 'description',
                  'creator', 'assigne_a', 'status',
                  'priority', 'balise']


class ProjectDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    contributors = ContributorSerializer(many=True, read_only=True)
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'creator',
                  'date_created', 'description',
                  'issues', 'contributors']
