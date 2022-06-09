from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'tag', 'name', 'birth_date', 'phone_num', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('birth_date', 'tag', 'name', 'profile_pic', 'self_intro', 'phone_num')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'tag', 'birth_date', 'name', 'profile_pic', 'self_intro', 'phone_num',
                       'is_admin', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'tag',)
    ordering = ('email', 'tag',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
