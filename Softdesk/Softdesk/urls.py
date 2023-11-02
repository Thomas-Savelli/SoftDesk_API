"""
URL configuration for Softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from API.views import (ListProjectsView,
                       user_registration_view,
                       join_project,
                       ProjectView,
                       IssueView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/signup/', user_registration_view, name='api_signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/project/', ListProjectsView.as_view({'post': 'create', 'get': 'list'}), name='project-list'),
    path('api/project/<int:id>/join/', join_project, name='join-project'),
    path('api/project/<int:id>/', ProjectView.as_view(), name='project_detail'),
    path('api/project/<int:project_id>/create_issue/', IssueView.as_view(), name='create-issue'),
    path('api/issue/<int:issue_id>/', IssueView.as_view(), name='retrieve-update-delete-issue'),
    # path('api/project/<int:project_id>/issue/create/', CreateIssueView.as_view(), name='issue-create'),
    # path('api/issue/update/<int:pk>/', UpdateIssueView.as_view(), name='upadate-issue'),
    # path('api/issue/delete/<int:pk>/', DeleteIssueView.as_view(), name='delete-issue'),
    # path('api/project/<int:project_id>/issue/<int:issue_id>/comment/create/', CreateCommentView.as_view(),
    #      name='create-comment'),
    # path('api/comment/update/<int:pk>/', UpdateCommentView.as_view(), name='update-comment'),
    # path('api/comment/delete/<int:pk>/', DeleteCommentView.as_view(), name='delete-comment'),
]
