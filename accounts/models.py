from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.core.validators import RegexValidator
from django.urls import reverse
from config.asset_storage import ProfileStorage
from config.settings import STATIC_URL
from django_fields import DefaultStaticImageField

class UserManager(BaseUserManager):
    def create_user(self, email, name, tag, birth_date, profile_pic, self_intro, phone_num, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            birth_date=birth_date,
            tag=tag,
            profile_pic=profile_pic,
            self_intro=self_intro,
            phone_num=phone_num,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, tag, phone_num, password):
        user = self.create_user(
            email=email,
            password=password,
            tag=tag,
            phone_num=phone_num,
            name="관리자",
            birth_date="1999-11-11",
            profile_pic="images/default_user_icon.png",
            self_intro="I'm Admin",
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):

    def profile_pic_upload(instance, filename):
        extension = filename.split(".")[-1]
        return f'profile_pic/{instance.tag}.{extension}'

    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(blank=False, default="", max_length=50)
    tag = models.CharField(blank=False, unique=True, max_length=25)
    birth_date = models.DateField()
    profile_pic = DefaultStaticImageField(storage=ProfileStorage(), upload_to=profile_pic_upload, blank=True,
                                          default_image_path='images/default_user_icon.png')
    self_intro = models.CharField(blank=True, max_length=255)
    regex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)([0-9]{3,4})([0-9]{4})$')
    phone_num = models.CharField(validators=[regex], max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['tag', 'phone_num']


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse('accounts:user_detail', args=[self.email])

    @property
    def is_staff(self):
        return self.is_admin

