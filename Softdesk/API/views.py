from rest_framework.generics import (CreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from django.contrib.auth.hashers import make_password
from datetime import date
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status, generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User, Project, Contributor, Issue, Comment
from .serializers import (UserSerializer,
                          UserDetailSerializer,
                          ProjectListSerializer,
                          ProjectDetailSerializer,
                          UserRegistrationSerializer,
                          ProjectSerializer,
                          IssueSerializer,
                          CommentSerializer)

from .permissions import IsContributor, IsCreator


@api_view(['POST'])
def user_registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Récupérer la date de naissance depuis les données du formulaire
            birthdate = serializer.validated_data.get('birthdate')
            
            if 'date_of_birth' in serializer.validated_data:
                birthdate = serializer.validated_data['date_of_birth']
                today = date.today()
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                if age < 15:
                    return Response({'message': 'You must be at least 15 years old to register.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'The date of birth is required.'}, status=status.HTTP_400_BAD_REQUEST)
            # Hacher le mot de passe avant de l'enregistrer
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
            return Response({'message': 'User registered successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get User Profile
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Update User Profile
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Delete User profile
        user = self.request.user
        user.delete()
        return Response({'message': 'Compte utilisateur supprimé avec succès'},
                        status=status.HTTP_204_NO_CONTENT)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'


class CustomListProjectsViewMixin:
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(creator=request.user)
            Contributor.objects.create(project=project, contributor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([IsAuthenticated])
class ListProjectsView(CustomListProjectsViewMixin, ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_project(request, id):
    try:
        project = Project.objects.get(pk=id)
        user = request.user
    except Project.DoesNotExist:
        return Response({"message": "Project does not exist"},
                        status=status.HTTP_404_NOT_FOUND)

    if Contributor.objects.filter(project=project, contributor=user).exists():
        return Response({"message": "You are already a contributor to this project"},
                        status=status.HTTP_400_BAD_REQUEST)

    Contributor.objects.create(project=project, contributor=user)
    return Response({"message": "Your request to become a contributor has been accepted"},
                    status=status.HTTP_201_CREATED)


class ProjectView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsContributor]

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.creator == request.user:
            project.delete()
            return Response({"detail": "Project successfully deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission to delete this project !"},
                        status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        project = self.get_object()
        if project.creator == self.request.user:
            serializer.save()
        else:
            return Response({"detail": "You do not have permission to update this project !"},
                            status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CreateIssueView(CreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')  # get ID Project
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # control if user is a contributor of Project
        if not Contributor.objects.filter(project=project, contributor=request.user).exists():
            return Response({"message": "You are not a contributor to this project"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user, project=project)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class IssueView(RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsAuthenticated, IsContributor]

    def get_object(self):
        # to config and select id of issue
        issue_id = self.kwargs.get('issue_id')
        try:
            issue = Issue.objects.get(id=issue_id)
            return issue
        except Issue.DoesNotExist:
            return Response({"message": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.creator == request.user:
            issue.delete()
            return Response({"detail": "Issue successfully deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission to delete this issue !"},
                        status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        issue = self.get_object()
        if issue.creator == self.request.user:
            serializer.save()
        else:
            return Response({"detail": "You do not have permission to update this issue !"},
                            status=status.HTTP_403_FORBIDDEN)


class CreateCommentView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_id')
        user = self.request.user

        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return Response({"message": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

        # check if user is contributor to project issue
        project = issue.project
        contributor = Contributor.objects.filter(project=project, contributor=user).first()

        if contributor:
            serializer.save(creator=contributor, issue=issue, link_issue=issue)
        else:
            return Response({"message": "You are not a contributor to this project and cannot create a comment"},
                            status=status.HTTP_403_FORBIDDEN)


class CommentView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def retrieve(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.creator.contributor.user == request.user:
            serializer = self.get_serializer(comment)
            return Response(serializer.data)
        else:
            return Response({"detail": "Vous n'avez pas la permission de consulter ce commentaire."}, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.creator.contributor.user == self.request.user:
            serializer.save()
            return Response({"detail": "Le commentaire a été mis à jour."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Vous n'avez pas la permission de mettre à jour ce commentaire."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.creator.contributor.user == request.user:
            comment.delete()
            return Response({"detail": "Le commentaire a été supprimé."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Vous n'avez pas la permission de supprimer ce commentaire."}, status=status.HTTP_403_FORBIDDEN)