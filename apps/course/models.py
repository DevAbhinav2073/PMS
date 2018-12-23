from django.db import models


# Create your models here.


class Stream(models.Model):
    stream_name = models.CharField(max_length=80)

    def __str__(self):
        return self.stream_name


class ElectiveSubject(models.Model):
    subject_name = models.CharField(max_length=80)
    min_student = models.IntegerField()
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT)

    def __str__(self):
        return self.subject_name
