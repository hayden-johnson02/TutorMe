from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    email = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    # https://docs.djangoproject.com/en/4.1/ref/models/instances/#:~:text=To%20create%20a%20new%20instance,you%20need%20to%20save()%20.
    @classmethod
    def create(cls, user, usertype):
        profile = cls(user=user, email=user.email, first_name=user.first_name, last_name=user.last_name)
        if usertype == "Student":
            Student.create(profile=profile)
        if usertype == "Tutor":
            Tutor.create(profile=profile)
        return profile


class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)


class Tutor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)