from django.contrib import admin
from hexanhome.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from hexanhome.forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','ip_adress')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Capteur)
admin.site.register(Type)
admin.site.register(Piece)
admin.site.register(Attribut)
admin.site.register(Actionneur)
admin.site.register(Attr_Capteur)
admin.site.register(RuleProfile)
admin.site.register(RuleAction)
admin.site.register(PresenceRule)
admin.site.register(TimeRule)
admin.site.register(TemperatureRule)
admin.site.register(WeatherRule)
admin.site.register(WeekdayRule)