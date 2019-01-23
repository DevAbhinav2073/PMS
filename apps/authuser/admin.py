import csv
import io

from django.contrib import admin, messages
# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db import IntegrityError
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.authuser.forms import NewStudentCreateForm, StudentChangeForm, DetailsForUploadingCSVForm, NAME_FIELD, \
    ROLL_NUMBER_FIELD, EMAIL_FIELD
from apps.authuser.models import StudentProxyModel, User

User = get_user_model()


class StudnetAdmin(UserAdmin):
    add_form = NewStudentCreateForm
    form = StudentChangeForm
    search_fields = ('name', 'username', 'email', 'roll_number')
    list_display = ('name', 'username', 'email', 'roll_number', 'batch', 'stream', 'level')
    list_filter = ()
    change_list_template = 'admin/authuser/authuser_student_change_list.html'
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

    def get_urls(self, *args, **kwargs):
        urls = super().get_urls(*args, **kwargs)
        custom_urls = [
            path('upload-student-csv', self.admin_site.admin_view(self.handle_csv_upload), name='handle-csv-upload')
        ]
        return custom_urls + urls

    @staticmethod
    def create_student_record_from_uploaded_csv(csv_file, academic_level, batch, faculty):
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string, delimiter=',', quotechar='|')
        list_of_created_username = []
        for row in reader:
            name = row.get(NAME_FIELD)
            roll_number = row.get(ROLL_NUMBER_FIELD)
            email = row.get(EMAIL_FIELD)

            try:
                user = User.objects.create(username=roll_number, name=name, roll_number=roll_number,
                                           level=academic_level, email=email,
                                           batch=batch, stream=faculty, user_type='Student')
                print(faculty)
                print(user.id)
                list_of_created_username.append(roll_number)
            except IntegrityError as e:
                for username in list_of_created_username:
                    User.objects.get(username=username).delete()
                raise IntegrityError(
                    'A student with roll number %s is already registered. Please handle this manually.' % (
                        roll_number,))

    def handle_csv_upload(self, request, *args, **kwargs):
        context = self.admin_site.each_context(request)
        if request.method != 'POST':
            form = DetailsForUploadingCSVForm
        else:
            form = DetailsForUploadingCSVForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    academic_level = form.cleaned_data.get('academic_level')
                    batch = form.cleaned_data.get('batch')
                    faculty = form.cleaned_data.get('faculty')
                    csv_file = request.FILES['csv_file']
                    self.create_student_record_from_uploaded_csv(csv_file, academic_level, batch, faculty)
                except Exception as e:
                    self.message_user(request, 'Failure: ' + str(e), messages.ERROR)

        context['opts'] = self.model._meta
        context['form'] = form
        context['title'] = 'Upload csv with students detail'
        return TemplateResponse(
            request,
            'admin/authuser/upload_csv.html',
            context,
        )


admin.site.register(StudentProxyModel, StudnetAdmin)
# admin.site.register(User)

admin.site.site_header = 'Elective Priority Management System'
admin.site.site_title = 'EPMS Admin'
admin.site.site_url = 'https://epms.abhinavdev.com.np/'
admin.site.index_title = 'Elective Priority Management System'
admin.empty_value_display = '----'
