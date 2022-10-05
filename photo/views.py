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
from .forms import *
from .serializers import *
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
            PostAndPhotoFormSet.extra = 1
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
    model = Post
    success_url = '/'
    template_name = 'photo/delete.html'

    def test_func(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return self.request.user == post.author or self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return HttpResponse('로그인 해주세요.')
        else:
            return HttpResponse('잘못된 요청입니다.')


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'photo/update.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['photos'] = PostAndPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            PostAndPhotoFormSet.extra = 0
            context['photos'] = PostAndPhotoFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['photos']
        with transaction.atomic():
            self.object = form.save()
            if images.is_valid():
                images.instance = self.object
                images.save()

        return super(PhotoUpdateView, self).form_valid(form)

    def test_func(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return self.request.user == post.author or self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return HttpResponse('로그인 해주세요.')
        else:
            return HttpResponse('잘못된 요청입니다.')


class PhotoDetailView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'photo/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        context['photos'] = Photo.objects.filter(post=self.object)
        return context


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
        return reverse_lazy('photo:photo_list_user', kwargs={'user_tag': self.request.POST['followname']})


@login_required
@api_view(('GET', 'POST'))
def photo_list(request): #팔로우 한 유저들의 게시글 로드
    page_num = int(request.POST.get('page_num')) if request.POST.get('page_num') != None else 1
    posts = Post.objects.prefetch_related('user_photos').all()
    follows_post = (posts.filter(author__in=Follow.objects.filter(user=request.user.id).values('follow')) |
                     posts.filter(author=request.user.id).order_by('-created'))[(page_num-1)*9:page_num*9]
    follows_post = follows_post.annotate(num_like=Count('like'))\
        .annotate(bool_like=Exists(Like.objects.filter(post=OuterRef('id'), user=request.user.id)))

    return render(request, 'photo/list.html', {'posts': follows_post})


@login_required
@api_view(('GET','POST'))
def photo_list_user(request, user_tag): #특정 유저의 게시글 로드
    page_num = int(request.POST.get('page_num')) if request.POST.get('page_num')!=None else 1
    this_user = get_object_or_404(User, tag=user_tag)
    followed = None
    followed_tmp = Follow.objects.filter(user=request.user, follow=this_user)
    followers = Follow.objects.filter(follow=this_user).count()
    followings = Follow.objects.filter(user=this_user).count()
    if followed_tmp.count():
        followed = followed_tmp[0]

    posts = Post.objects.prefetch_related('user_photos').filter(author=this_user).order_by('-created')[(page_num-1)*9:page_num*9]
    posts = posts.annotate(num_like=Count('like')) \
        .annotate(bool_like=Exists(Like.objects.filter(post=OuterRef('id'), user=request.user.id)))
    return render(request, 'photo/mypage.html',
                  {'posts': posts, 'this_user': this_user,
                   'followers': followers, 'followings': followings, 'followed': followed})

@login_required
@api_view(('GET',))
def search_user(request, user_tag):
    users = User.objects.filter(tag__istartswith=user_tag)[:5]
    if users.count() == 0:
        users = User.objects.filter(tag__icontains=user_tag)[:5]
    #users = get_users.delay(user_name)
    return Response(data=UserNameSerializer(users, many=True).data)

@login_required
def like_photo(request, post_id):
    post = Post.objects.get(id=post_id)
    Like.objects.create(post=post, user=request.user).save()
    likes = Like.objects.filter(post=post).count()
    return HttpResponse(likes)

@login_required
def unlike_photo(request, post_id):
    Like.objects.filter(post=post_id, user=request.user).delete()
    likes = Like.objects.filter(post=post_id).count()
    return HttpResponse(likes)

@login_required
@api_view(('GET',))
def followers_list(request, user_tag):
    user = get_object_or_404(User, tag=user_tag)
    followers = User.objects.filter(id__in=Follow.objects.filter(follow=user).values('user'))
    return Response(data=UserNameSerializer(followers, many=True).data)

@login_required
@api_view(('GET',))
def followings_list(request, user_tag):
    user = get_object_or_404(User, tag=user_tag)
    followings = User.objects.filter(id__in=Follow.objects.filter(user=user).values('follow'))
    return Response(data=UserNameSerializer(followings, many=True).data)
