from django.contrib import admin

# Register your models here.
from apps.course.models import ElectiveSubject, Stream


class StreamAdmin(admin.ModelAdmin):
    pass


class ElectiveSubjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(ElectiveSubject, ElectiveSubjectAdmin)
admin.site.register(Stream, StreamAdmin)
