from django.db import models
from accounts.models import User
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, Transpose


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.tag + " " + self.created.strftime('%Y-%m-%d %H:%M:%S')

    def get_absolute_url(self):
        return reverse('photo:photo_detail',args=[str(self.id)])


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='user_photos')
    #photo = models.ImageField(upload_to='photos/%Y/%m/%d', default='photos/no_image.png')
    photo = ProcessedImageField(upload_to='photos/%Y/%m/%d',
                                           processors=[Transpose(), #변환 후 rotate 방지
                                                       ResizeToFill(470, 470)],
                                           format='JPEG',
                                           options={'quality': 60})
    #imagekit을 사용해 이미지 resize


class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_following')
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follows')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.tag + "님이 " + self.follow.tag + "님을 팔로우했습니다.(" + self.created.strftime('%Y-%m-%d %H:%M:%S') + ")"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)