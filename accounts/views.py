from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import User
from django.views.generic.edit import *
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse
# Create your views here.


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['name', 'tag', 'birth_date', 'phone_num', 'self_intro', 'profile_pic']
    template_name = 'registration/update.html'
    success_url = '/mypage/{tag}'

    def get_object(self):
        object = get_object_or_404(User, email=self.kwargs['user_id'])
        return object

    def test_func(self):
        user = get_object_or_404(User, email=self.kwargs['user_id'])
        return self.request.user == user or self.request.user.is_admin or self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return HttpResponse('로그인 해주세요.')
        else:
            return HttpResponse('잘못된 요청입니다.')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'registration/delete.html'
    success_url = '/'

    def get_object(self):
        object = get_object_or_404(User, email=self.kwargs['user_id'])
        return object

    def test_func(self):
        user = get_object_or_404(User, email=self.kwargs['user_id'])
        return self.request.user == user or self.request.user.is_admin or self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return HttpResponse('로그인 해주세요.')
        else:
            return HttpResponse('잘못된 요청입니다.')


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.profile_pic = request.FILES.get('profile_pic')
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': user_form})
