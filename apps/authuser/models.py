from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
from apps.course.models import Stream

USER_TYPE_CHOICES = (
    ('Student', 'Student'),
    ('Staff', 'Staff')
)


class StudentObjectsManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='Student')


class User(AbstractUser):
    stream = models.ForeignKey(Stream, null=True, blank=True, on_delete=models.PROTECT)
    roll_number = models.CharField(max_length=30)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=30, default='Staff')


class StudentProxyModel(User):
    objects = StudentObjectsManager()

    def __str__(self):
        return '%s (%s)' % (self.get_full_name(), self.username)

    class Meta:
        proxy = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
