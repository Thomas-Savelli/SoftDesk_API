from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, RetrieveAPIView
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Project, Contributor, Issue
from .serializers import (ProjectListSerializer,
                          ProjectDetailSerializer,
                          UserRegistrationSerializer,
                          ProjectSerializer,
                          IssueSerializer)

from .permissions import IsContributor, IsProjectCreator


@api_view(['POST'])
def user_registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Hacher le mot de passe avant de l'enregistrer
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
            return Response({'message': 'User registered successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ListProjectsView(viewsets.ReadOnlyModelViewSet):
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


@permission_classes([IsAuthenticated, IsContributor])
class DetailProjectView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CreateProjectView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class ProjectUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectCreator]
    http_method_names = ['put', 'patch']


class ProjectDeleteAPIView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectCreator]

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.creator == request.user:
            project.delete()
            return Response({"detail": "Project successfully deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission to delete this project !"},
                        status=status.HTTP_403_FORBIDDEN)


class CreateIssueView(CreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def perform_create(self, serializer):
        # Récupérez le projet auquel l'issue doit être associée
        project_id = self.kwargs.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"message": "The project does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        if project.contributors.filter(id=self.request.user.id).exists():
            serializer.save(project=project, creator=self.request.user)
        else:
            return Response({"message": "You are not allowed to create an issue in this project."},
                            status=status.HTTP_403_FORBIDDEN)
