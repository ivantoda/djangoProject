"""
URL configuration for projekt project.

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
from django.contrib.auth.views import LoginView, LogoutView
from app_1 import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_user/', views.add_user, name='add_user'),
    path('update_user/<int:id>', views.update_user, name='update_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('administrator/<int:id>/', views.admin_view, name='administrator'),
    path('profesor/<int:id>/', views.profesor_view, name='profesor'),
    path('add_document/', views.add_document, name='add_document'),
    path('update_document/<int:id>', views.update_document, name='update_document'),
    path('delete_document/<int:id>', views.delete_document, name='delete_document'),
    path('share_document/<int:id>', views.share_document, name='share_document'),
    path('student/<int:id>/', views.student_view, name='student'),
    path('download_file/<path:file_path>/', views.download_file, name='download_file'),
    path('ispit/', views.ispit, name='ispit'),
    path('ispit2/', views.ispit2, name='ispit2')
    #path('admin_test/<name>/<int:count>', views.admin_next, name='admin_next'),
    #path('admin_exercise/', views.admin_exercise, name='admin_exercise'),
]
