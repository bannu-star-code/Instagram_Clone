"""igprj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from authy.views import UserProfile, EditProfile, follow, register, follower_list, following_list
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users/', include('authy.urls')),
    # user AUthentication
    path('sign-up/', register, name='sign-up'),
    path('sign-in/', auth_views.LoginView.as_view(template_name='sign-in.html', redirect_authenticated_user=True), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name='sign-out.html'), name='sign-out'),
    path('', include('post.urls')),
    path('message/', include('directs.urls')),
    path('<username>/',UserProfile,name='profile'),
    path('<username>/saved',UserProfile,name='profilefavourite'),
    path('profile/edit', EditProfile, name="editprofile"),
    path('<username>/follow/<option>/',follow, name='follow'),
    path('<username>/followers', follower_list, name='follower_list'),
    path('<username>/following', following_list, name='following_list'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
