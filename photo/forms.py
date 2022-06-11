from django import forms
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)


PostAndPhotoFormSet = forms.models.inlineformset_factory(Post, Photo, fields=('photo',), max_num=10, extra=1)
