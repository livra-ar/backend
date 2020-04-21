from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .forms import ModeratorCreationForm, ModeratorChangeForm
from .models import Moderator


class ModeratorAdmin(UserAdmin):
    add_form = ModeratorCreationForm
    form = ModeratorChangeForm
    model = Moderator
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Moderator, ModeratorAdmin)