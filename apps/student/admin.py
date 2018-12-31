from django.contrib import admin

# Register your models here.
from apps.student.forms import PriorityForm
from apps.student.models import ElectivePriority


class ElectivePriorityAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(student=request.user)


admin.site.register(ElectivePriority, ElectivePriorityAdmin)
