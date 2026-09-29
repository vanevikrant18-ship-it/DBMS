from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    age = models.IntegerField(default=0)
    qualification = models.CharField(max_length=100, default="")
    skills = models.TextField(default="")

    def __str__(self):
        return self.user.username


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    required_skills = models.TextField()
    qualification_required = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


class Interview(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    interview_date = models.DateField()

    def __str__(self):
        return f"{self.student.user.username} - {self.company_name}"