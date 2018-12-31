from django.contrib import admin

# Register your models here.
from apps.course.models import ElectiveSubject, Stream, Batch, ElectiveSession, AcademicLevel


class StreamAdmin(admin.ModelAdmin):
    pass


class ElectiveSubjectAdmin(admin.ModelAdmin):
    pass


class BatchAdmin(admin.ModelAdmin):
    pass


class LevelAdmin(admin.ModelAdmin):
    pass


class ElectiveSessionAdmin(admin.ModelAdmin):
    pass


admin.site.register(ElectiveSubject, ElectiveSubjectAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(AcademicLevel, LevelAdmin)
admin.site.register(ElectiveSession, BatchAdmin)
