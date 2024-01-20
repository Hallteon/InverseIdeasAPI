"""
URL configuration for HelloDjango project.

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
from django.urls import path
from django.conf.urls.static import static
from companies.views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from postideas.settings import MEDIA_ROOT, MEDIA_URL
from proposals.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from users.views import *
from proposals.views import *


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Companies
    path('api/companies/offices/', OfficeAPIListView.as_view(), name='offices_list'),
    path('api/companies/offices/departments/divisions/', DivisionAPIGetListView.as_view(), name='divisions_list'),
    
    # Proposals
    path('api/proposals/create/', ProposalAPICreateView.as_view(), name='proposal_create'),
    path('api/proposals/<int:pk>/', ProposalAPIDetailView.as_view(), name='proposal_detail'),
    path('api/proposals/heads/', ProposalAPIGetHeadsView.as_view(), name='proposal_level_heads_get'),
    path('api/proposals/<int:pk>/approve/', ProposalAPIApproveView.as_view(), name='proposal_approve'),
    path('api/proposals/<int:pk>/reject/', ProposalAPIRejectView.as_view(), name='proposal_reject'),
    path('api/proposals/<int:pk>/execute/', ProposalAPIExecuteView.as_view(), name='proposal_execute'),
    path('api/proposals/<int:pk>/process/', ProposalAPIProcessView.as_view(), name='proposal_process'),
    path('api/proposals/<int:pk>/revision/', ProposalAPIRevisionView.as_view(), name='proposal_revision'),
    path('api/proposals/statuses/', StatusAPIListView.as_view(), name='proposal_statuses'),
    path('api/proposals/categories/', CategoryAPIListView.as_view(), name='proposals_categories_get'),
    path('api/proposals/me/', ProposalAPIListMeView.as_view(), name='proposals_me'),
    path('api/proposals/me/search/', ProposalAPIListSearchView.as_view(), name='proposals_search'),
    path('api/proposals/posts/', ProposalPostAPIListView.as_view(), name='proposal_posts_get_all'),
    path('api/proposals/posts/<int:pk>/', ProposalPostAPIDetailView.as_view(), name='proposal_post_detail_get'),
    path('api/proposals/<int:pk>/comments/create/', ProposalPostAPICreateCommentView.as_view(), name='proposal_comment_create'),
    path('api/proposals/<int:pk>/likes/add/', ProposalPostAPIAddLikesView.as_view(), name='proposal_posts_like_add'),
    
    # Users
    path('api/users/me/', CurrentUserAPIDetailView.as_view(), name='current_user'),
    path('api/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)