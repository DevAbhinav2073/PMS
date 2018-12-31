from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from apps.authuser.forms import NewStudentCreateForm, StudentChangeForm
from apps.authuser.models import StudentProxyModel


class StudnetAdmin(UserAdmin):
    add_form = NewStudentCreateForm
    form = StudentChangeForm
    search_fields = ('first_name', 'last_name', 'username', 'email', 'roll_number')
    list_display = ('first_name', 'last_name', 'username', 'email', 'roll_number', 'batch', 'stream')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'batch', 'stream', 'roll_number')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name', 'last_name', 'email', 'roll_number', 'username', 'batch', 'stream',),
        }),
    )
    prepopulated_fields = {'username': ('roll_number',)}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return super().get_queryset(request)
        return queryset.filter(id=request.user.id)


admin.site.register(StudentProxyModel, StudnetAdmin)

admin.site.site_header = 'Elective Priority Management System'
admin.site.site_title = 'EPMS Admin'
admin.site.site_url = 'https://epms.abhinavdev.com.np/'
admin.site.index_title = 'Elective Priority Management System'
admin.empty_value_display = '----'
