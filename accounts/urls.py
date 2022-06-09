from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'),name='logout'),
    path('register/', register, name='register'),
    path('update/<str:user_id>', UserUpdateView.as_view(), name='user_update'),

]
