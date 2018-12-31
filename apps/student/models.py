from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.db import models

# Create your models here.
from apps.authuser.models import StudentProxyModel
from apps.course.models import Stream, ElectiveSubject

User = get_user_model()




class ElectivePriority(models.Model):
    subject = models.ForeignKey(ElectiveSubject, on_delete=models.CASCADE)
    priority = models.IntegerField()
    student = models.ForeignKey(StudentProxyModel, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('subject', 'priority', 'student')
        verbose_name = 'Priority'
        verbose_name_plural = 'Priorities'

    def __str__(self):
        return '%s has priority %d' % (self.subject.subject_name
                                       , self.priority)
