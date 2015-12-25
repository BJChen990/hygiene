from django.db import models

# Create your models here.
class Class(models.Model):
    grade = models.TextField()
    number = models.PositiveSmallIntegerField(default=0)
    name = models.TextField(default=None)
    type = models.TextField(max_length=20)

class Student(models.Model):
    id_in_class = models.PositiveSmallIntegerField(default=0)
    name = models.TextField(max_length=20)
    gender = models.TextField(max_length=10)
    student_id = models.TextField(max_length=20)
    the_class = models.ForeignKey(Class, default=None)
    times_remain_to_clean = models.PositiveSmallIntegerField(default=3)
    date_to_come = models.TextField(max_length=60, default='[]')