from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.student.models import StudentProxyModel

User = get_user_model()

STUDENT_GROUP_NAME = 'STUDENT'


@receiver(post_save, sender=StudentProxyModel)
def create_student_account(sender, instance, created, *args, **kwargs):
    if created:
        instance.user_type = 'Student'
        instance.is_staff = True
        instance.save()
        student_group, created = Group.objects.get_or_create(name=STUDENT_GROUP_NAME)
        instance.groups.add(student_group)
