from django.db import models


class Student(models.Model):
    level_id = models.IntegerField(blank=0)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birthdate = models.CharField(max_length=50)
    livesin = models.CharField(max_length=50)
    school = models.IntegerField(blank=0)
    grade = models.IntegerField(blank=0)
    siblings = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='student_pictures', blank='True')
    notes = models.CharField(max_length=1000)


class Levels(models.Model):
    period = models.CharField(max_length=30)
    level = models.CharField(max_length=30)
    status = models.BooleanField(default=True)


class School(models.Model):
    name = models.CharField(max_length=50)


class Grade(models.Model):
    name = models.CharField(max_length=15)



