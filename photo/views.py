from django.shortcuts import render,redirect
from .models import *
from django.views.generic.edit import *
from django.contrib.auth.decorators import *
from django.contrib.auth.mixins import *
# Create your views here.

class PhotoUploadView(LoginRequiredMixin,CreateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/upload.html'
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save();
            return redirect('/')
        else:
            return self.render_to_response({'form' : form})

class PhotoDeleteView(LoginRequiredMixin,DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'

class PhotoUpdateView(LoginRequiredMixin,UpdateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/update.html'

class PhotoDetailView(LoginRequiredMixin,DeleteView):
    model = Photo
    template_name='photo/detail.html'

@login_required
def photo_list(request):
    photos = Photo.objects.all()
    return render(request,'photo/list.html', {'photos': photos})
