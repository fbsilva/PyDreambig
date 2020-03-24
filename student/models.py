from django.db import models


class Student(models.Model):
    level_id = models.IntegerField(blank=0)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birthDate = models.CharField(max_length=50)
    livesIn = models.CharField(max_length=50)
    school = models.IntegerField(blank=0)
    grade = models.IntegerField(blank=0)
    siblings = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='media/', default='')
    notes = models.CharField(max_length=1000)
    createdAt = models.DateTimeField(default='1900-01-01 00:00:00')
    modifiedAt = models.DateTimeField(default='1900-01-01 00:00:00')
    deleted = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=35, default='admin')


class Levels(models.Model):
    period = models.CharField(max_length=30)
    level = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    createdAt = models.DateTimeField(default='1900-01-01 00:00:00')
    modifiedAt = models.DateTimeField(default='1900-01-01 00:00:00')
    deleted = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=35, default='admin')


class School(models.Model):
    name = models.CharField(max_length=50)
    createdAt = models.DateTimeField(default='1900-01-01 00:00:00')
    modifiedAt = models.DateTimeField(default='1900-01-01 00:00:00')
    deleted = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=35, default='admin')


class Grade(models.Model):
    name = models.CharField(max_length=15)
    createdAt = models.DateTimeField(default='1900-01-01 00:00:00')
    modifiedAt = models.DateTimeField(default='1900-01-01 00:00:00')
    deleted = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=35, default='admin')


class StudentsLevelHistorical(models.Model):
    studentId = models.IntegerField(blank=0)
    levelId = models.IntegerField(blank=0)
    createdAt = models.DateTimeField(default='1900-01-01 00:00:00')
    createdBy = models.CharField(max_length=35, default='admin')
