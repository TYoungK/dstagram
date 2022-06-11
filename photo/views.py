from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.views.generic.edit import *
from django.contrib.auth.decorators import *
from django.contrib.auth.mixins import *
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse
from .tasks import *
from accounts.serializers import UserNameSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Count, Exists, OuterRef
from django.db import transaction
from django.contrib.postgres.aggregates.general import ArrayAgg
from accounts.models import User
from .forms import *
# Create your views here.

class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'photo/upload.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PhotoUploadView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['photos'] = PostAndPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['photos'] = PostAndPhotoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['photos']
        form.instance.author_id = self.request.user.id
        with transaction.atomic():
            self.object = form.save()
            if images.is_valid():
                images.instance = self.object
                images.save()

        return super(PhotoUploadView, self).form_valid(form)


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'

    def test_func(self):
        photo = get_object_or_404(Photo, id=self.kwargs['pk'])
        return self.request.user == photo.author or self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return HttpResponse('로그인 해주세요.')
        else:
            return HttpResponse('잘못된 요청입니다.')


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/update.html'

    def test_func(self):
        photo = get_object_or_404(Photo, id=self.kwargs['pk'])
        return self.request.user == photo.author or self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return HttpResponse('로그인 해주세요.')
        else:
            return HttpResponse('잘못된 요청입니다.')


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
        return reverse_lazy('photo:photo_list_user', kwargs={'user_id': self.request.POST['followname']})

@login_required
@api_view(('GET', 'POST'))
def photo_list(request): #팔로우 한 유저들의 게시글 로드
    page_num = int(request.POST.get('page_num')) if request.POST.get('page_num') != None else 1
    posts = Post.objects.prefetch_related('user_photos').all()
    follows_post = (posts.filter(author__in=Follow.objects.filter(user=request.user.id).values('follow')) |
                     posts.filter(author=request.user.id).order_by('-created'))[(page_num-1)*10:page_num*10]
    follows_post = follows_post.annotate(num_like=Count('like'))\
        .annotate(bool_like=Exists(Like.objects.filter(post=OuterRef('id'), user=request.user.id)))

    #print(follows_post[0].user_photos.all()[0].photo)
    #follows_post = Photo.objects.filter(post__in=follows_post)
    #photos = Photo.objects.prefetch_related(follows)
    return render(request, 'photo/list.html', {'posts': follows_post})


@login_required
@api_view(('GET','POST'))
def photo_list_user(request, user_tag): #특정 유저의 게시글 로드
    page_num = int(request.POST.get('page_num')) if request.POST.get('page_num')!=None else 1
    this_user = get_object_or_404(User, tag=user_tag)
    followed = None
    follow_tmp = Follow.objects.filter(user=request.user, follow=this_user).order_by('-created')
    if follow_tmp.count():
        followed = follow_tmp[0]

    posts = Post.objects.prefetch_related('user_photos').filter(author=this_user)[(page_num-1)*10:page_num*10-1]
    #posts = posts.filter(author=this_user)[(page_num-1)*10:page_num*10-1]

    return render(request, 'photo/mypage.html', {'posts': posts, 'this_user': this_user, 'followed': followed})

@login_required
@api_view(('GET',))
def search_user(request, user_tag):
    users = User.objects.filter(tag__istartswith=user_tag)[:5]
    if users.count() == 0:
        users = User.objects.filter(tag__icontains=user_tag)[:5]
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