from django.urls import path
from django.views.generic.detail import DetailView
from .views import *
from .models import *

app_name = 'photo'

urlpatterns = [
    path('', photo_list, name='photo_list'),
    path('detail/<int:pk>', PhotoDetailView.as_view(), name='photo_detail'),
    path('upload/', PhotoUploadView.as_view(), name='photo_upload'),
    path('delete/<int:pk>', PhotoDeleteView.as_view(), name='photo_delete'),
    path('update/<int:pk>', PhotoUpdateView.as_view(), name='photo_update'),
    path('mypage/<str:user_tag>', photo_list_user, name='photo_list_user'),
    path('follow/<str:user_tag>', FollowingView.as_view(), name='follow'),
    path('unfollow/<int:pk>', UnFollowingView.as_view(), name='unfollow'),
    path('search/<str:user_tag>', search_user, name='search_user'),
    path('like/<int:post_id>', like_photo, name='like_photo'),
    path('unlike/<int:post_id>', unlike_photo, name='unlike_photo'),
    path('follower/<str:user_tag>', followers_list, name='follower'),
    path('following/<str:user_tag>', followings_list, name='following'),
]
