from django.db import models

# Create your models here.
class User(models.Model):
    password = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20)
    type = models.CharField(max_length=20, default='manager')


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
    should_come_count = models.PositiveSmallIntegerField(default=3)
    date_schedule = models.TextField(max_length=60, default='{}')
