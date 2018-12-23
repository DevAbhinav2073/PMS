from django.contrib import admin

# Register your models here.

from apps.student.models import  ElectivePriority


class ElectivePriorityAdmin(admin.ModelAdmin):
    pass


admin.site.register(ElectivePriority, ElectivePriorityAdmin)
