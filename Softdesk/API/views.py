from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Project, Contributor
from .serializers import (ProjectListSerializer,
                          ProjectDetailSerializer,
                          UserRegistrationSerializer)
from .permissions import IsContributor


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


class DetailProjectsView(generics.RetrieveAPIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        project_id = self.kwargs['id']
        return Project.objects.filter(id=project_id).prefetch_related('issues', 'contributors')
