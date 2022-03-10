from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Photo(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_photos')
    photo = models.ImageField(upload_to = 'photos/%Y/%m/%d', default='photos/no_image.png')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime('%Y-%m-%d %H:%M:%S')

    def get_absolute_url(self):
        return reverse('photo:photo_detail',args=[str(self.id)])
    
class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following')
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follows')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + "님이 " + self.follow.username + "님을 팔로우했습니다.(" + self.created.strftime('%Y-%m-%d %H:%M:%S') + ")"

class Like(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)