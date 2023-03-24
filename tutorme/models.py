from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256, blank=False)
    last_name = models.CharField(max_length=256)
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    bio = models.TextField(max_length=1200, blank=True, null=True, default=None)

    # tutor specific
    hourly_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)],
                                      blank=True, null=True, default=None)
    venmo = models.CharField(max_length=256, blank=True, null=True, default=None)

    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, email=instance.email,
                                   first_name=instance.first_name, last_name=instance.last_name)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    
    def __delete__(self):
        self.user.delete()


class Course(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=4)
    catalog_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    course_name = models.CharField(max_length=256)


class TutorSession(models.Model):
    DAYS_OF_WEEK = [('Monday', 'Monday'),
                    ('Tuesday', 'Tuesday'),
                    ('Wednesday', 'Wednesday'),
                    ('Thursday', 'Thursday'),
                    ('Friday', 'Friday'),
                    ('Saturday', 'Saturday'),
                    ('Sunday', 'Sunday')]
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    tutor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='TutorSession_tutor')


class TutorRequest(models.Model):
    tutor_session = models.ForeignKey(TutorSession, on_delete=models.CASCADE)
    description = models.TextField(max_length=600)  # Student should put course they want help for in this description
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='TutorRequest_student')
    date = models.DateField(auto_now=False, auto_now_add=False, default=None)
    is_accepted = models.BooleanField(default=None)
