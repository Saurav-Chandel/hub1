"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app.views import Login
from django.contrib.auth import login
from app.views import *
from app import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',auth_views.LoginView.as_view(), name='login'),
    # path('',Login.as_view(),name='login'),  
    path('',Login,name='login'),
    path('logout/',logout,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    path('BusinessManagement/',buisness_management,name='buisness_management'),
    path('report/',report_management,name='report_management'),
    path('UserManagement/',user_management,name='user_management'),
    # path('change_password/',views.Change_Password.as_view(),name='change_password'),
    path(
        'auth-change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='commons/change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += [] + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += [] + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    