from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.views.generic.edit import *
from django.contrib.auth.decorators import *
from django.contrib.auth.mixins import *
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse
from .tasks import *
from accounts.serializers import UserNameSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db.models import Count, Exists, OuterRef
from .serializers import PhotoSerializer

# Create your views here.

class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/update.html'


class PhotoDetailView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photo/detail.html'

class FollowingView(LoginRequiredMixin, CreateView):
    model = Follow
    fields = ['user','follow']
    template_name = 'photo/mypage.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id

        if form.is_valid():
            form.instance.save()
            return redirect('/mypage/'+self.request.POST['followname'])
        else:
            return self.render_to_response({'form': form})

class UnFollowingView(LoginRequiredMixin, DeleteView):
    model = Follow
    def get_success_url(self):
        return reverse_lazy('photo:photo_list_user',kwargs={'user_id': self.request.POST['followname']})

@login_required
@api_view(('GET','POST'))
def photo_list(request): #팔로우 한 유저의 게시글 로드
    page_num = int(request.POST.get('page_num')) if request.POST.get('page_num') != None else 1
    follows_photo = (Photo.objects.filter(author__in=Follow.objects.filter(user=request.user.id).values('follow')) | \
                    Photo.objects.filter(author=request.user).order_by('-created'))[(page_num-1)*10:page_num*10-1]
    follows_photo = follows_photo.annotate(num_like=Count('like'))\
        .annotate(bool_like=Exists(Like.objects.filter(photo=OuterRef('id'),user=request.user)))

    #photos = Photo.objects.prefetch_related(follows)
    return render(request, 'photo/list.html', {'photos': follows_photo})


@login_required
@api_view(('GET','POST'))
def photo_list_user(request, user_id): #특정 유저의 게시글 로드
    page_num = int(request.POST.get('page_num')) if request.POST.get('page_num') != None else 1
    this_user = get_object_or_404(User, username=user_id)
    followed = None
    follow_tmp = Follow.objects.filter(user=request.user, follow=this_user).order_by('-created')
    if follow_tmp.count():
        followed = follow_tmp[0]

    photos = Photo.objects.filter(author=this_user.id)[(page_num-1)*10:page_num*10-1]
    return render(request, 'photo/mypage.html', {'photos': photos,'this_user':this_user,'followed':followed})

@login_required
@api_view(('GET',))
def search_user(request, user_name):
    users = User.objects.filter(username__istartswith=user_name)[:5]
    if users.count() == 0:
        users = User.objects.filter(username__icontains=user_name)[:5]
    #users = get_users.delay(user_name)
    return Response(data=UserNameSerializer(users, many=True).data)

@login_required
def like_photo(request, photo_id):
    Like.objects.create(photo_id=photo_id, user=request.user).save()
    likes = Like.objects.filter(photo_id=photo_id).count()
    return HttpResponse(likes)

@login_required
def unlike_photo(request, photo_id):
    Like.objects.filter(photo_id=photo_id, user=request.user).delete()
    likes = Like.objects.filter(photo_id=photo_id).count()
    return HttpResponse(likes)