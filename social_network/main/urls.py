from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import profile
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.start_menu, name='start_menu'),
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
    path('news', views.HomeView.as_view(), name='news'),
    path('friends', views.FriendsView.as_view(), name='friends'),
    path('profile_page/<str:username>/', views.profile_page.as_view(), name='profile_page'),
    path('add_post', views.CreatePost.as_view(), name='add_post'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('edit_profile/', profile, name='users-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)