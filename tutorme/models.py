from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


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

    def average_rating(self):
        reviews = Review.objects.filter(tutor=self.user)
        if len(reviews) == 0:
            return 0
        else:
            return round(sum([review.rating for review in reviews]) / len(reviews),1)
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_email(self):
        return self.email
    
    def get_sessions(self):
        return TutorSession.objects.filter(tutor=self.user)

    def courses(self):
        return Course.objects.filter(profile=self)

    def __delete__(self):
        self.user.delete()

    def __str__(self):
        return f'Name: {self.first_name} {self.last_name}; Email: {self.email}; Is Tutor: {self.is_tutor}; Is Student: {self.is_student}; Bio: {self.bio}; Hourly Rate: {self.hourly_rate}; Venmo: {self.venmo}'


class Course(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=4)
    catalog_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    course_name = models.CharField(max_length=256)


class Review(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.reviewer}'

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
    date = models.DateField(default=datetime.date.today)

    def tutor_requests(self):
        return TutorRequest.objects.filter(tutor_session=self).exclude(status='Denied')
    
    def all_requests(self):
        return TutorRequest.objects.filter(tutor_session=self)
    

    def __str__(self):
        return f'{self.tutor} {self.day} {self.start_time} - {self.end_time}'


class TutorRequest(models.Model):
    tutor_session = models.ForeignKey(TutorSession, on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='TutorRequest_student')
    is_accepted = models.BooleanField(default=False)
    description = models.TextField(max_length=1200, default='No description provided.')
    status = models.CharField(max_length=256, default='Pending')
