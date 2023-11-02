from rest_framework.generics import (RetrieveUpdateAPIView,
                                     CreateAPIView, DestroyAPIView,
                                     RetrieveUpdateDestroyAPIView)

from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status, generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Project, Contributor, Issue, Comment
from .serializers import (ProjectListSerializer,
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
            # Hacher le mot de passe avant de l'enregistrer
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
            return Response({'message': 'User registered successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ProjectView(CreateAPIView, RetrieveUpdateDestroyAPIView):
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


class IssueView(CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView):
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

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"message": "The project does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.contributors.filter(id=self.request.user.id).exists():
            issue = serializer.save(project=project, creator=self.request.user)
            return Response({"message": "Issue created successfully", "issue_id": issue.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You are not allowed to create an issue in this project."}, status=status.HTTP_403_FORBIDDEN)

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


# class UpdateIssueView(RetrieveUpdateAPIView):
#     serializer_class = IssueSerializer
#     queryset = Issue.objects.all()
#     permission_classes = [IsAuthenticated, IsCreator]
#     http_method_names = ['put', 'patch']


# class DeleteIssueView(generics.DestroyAPIView):
#     queryset = Issue.objects.all()
#     serializer_class = IssueSerializer
#     permission_classes = [IsAuthenticated, IsCreator]

#     def destroy(self, request, *args, **kwargs):
#         issue = self.get_object()
#         if issue.creator == request.user:
#             issue.delete()
#             return Response({"detail": "Issue successfully deleted"},
#                             status=status.HTTP_204_NO_CONTENT)
#         return Response({"detail": "You do not have permission to delete this issue !"},
#                         status=status.HTTP_403_FORBIDDEN)


class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_id')
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return Response({"message": "The issue does not exist"}, status=status.HTTP_404_NOT_FOUND)

        contributor = Contributor.objects.get(user=self.request.user)
        if issue.project.contributors.filter(id=self.request.user.id).exists():
            serializer.save(issue=issue, creator=self.request.user)
        else:
            return Response({"message": "You are not allowed to create an issue in this project."},
                            status=status.HTTP_403_FORBIDDEN)


class UpdateCommentView(RetrieveUpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsCreator]
    http_method_names = ['put', 'patch']


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.creator == request.user:
            comment.delete()
            return Response({"detail": "Comment successfully deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission to delete this comment !"},
                        status=status.HTTP_403_FORBIDDEN)
