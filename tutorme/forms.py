from django import forms
from django.core.exceptions import ValidationError
import datetime
from django.utils.timezone import now, localtime
from .models import Profile, TutorSession, Review


class UserTypeForm(forms.Form):
    CHOICES = [
        ('1', 'Student'),
        ('2', 'Tutor'),
    ]
    options = forms.ChoiceField(widget=forms.RadioSelect,
                                choices=CHOICES)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = {'is_tutor', 'is_student'}
        fields = {'first_name', 'last_name', 'email', 'bio', 'hourly_rate', 'venmo'}

        # https://www.youtube.com/watch?v=6-XXvUENY_8 Styling
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'fname', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'lname', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'readonly class': 'form-control', 'id': 'email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-height: 300px;',
                                         'placeholder': 'Write some information about yourself!'}),
            'hourly_rate': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control',
                                                    'min': '0', 'max': '1000',
                                                    'id': 'hr', 'style': 'max-width: 110px;',
                                                    'placeholder': '25'}),
            'venmo': forms.TextInput(attrs={'class': 'form-control', 'id': 'venmo', 'placeholder': 'venmo_tag'}),
        }


# https://jacobian.org/2010/feb/28/dynamic-form-generation/
class DynamicCourseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('course_list')
        super(DynamicCourseForm, self).__init__(*args, **kwargs)

        choices = []
        for i, course_name in enumerate(extra):
            choices.append((course_name, course_name))
        self.fields['Select_Courses'] = forms.MultipleChoiceField(
            label="",
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=choices,
        )


class CreateSessionForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(CreateSessionForm, self).clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time.hour > end_time.hour:
            raise ValidationError("End time must be after start time")
        if end_time.hour == start_time.hour and start_time.minute >= end_time.minute:
            raise ValidationError("End time must be after start time")
        return cleaned_data

    class Meta:

        model = TutorSession
        exclude = {}
        fields = {'start_time', 'end_time', 'day'}
        DAYS_OF_WEEK = [('Monday', 'Monday'),
                        ('Tuesday', 'Tuesday'),
                        ('Wednesday', 'Wednesday'),
                        ('Thursday', 'Thursday'),
                        ('Friday', 'Friday'),
                        ('Saturday', 'Saturday'),
                        ('Sunday', 'Sunday')]
        widgets = {
            'day': forms.Select(choices=DAYS_OF_WEEK),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'})
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-range', 'type': 'range', 'min': '1', 'max': '5', 'step': '1',
                                        'id': 'rating'}),
            'comment': forms.Textarea(
                attrs={'class': 'form-control mt-3 mb-3', 'placeholder': 'Leave a review here!', 'style': 'height: 100px',
                       'id': 'comment'})
        }


class DynamicSessionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        session_id = kwargs.pop('sessionID')
        super(DynamicSessionForm, self).__init__(*args, **kwargs)

        session = TutorSession.objects.get(pk=int(session_id))

        choices = []
        start_day = None
        today = datetime.date.today()
        s_day = None
        if session.day == 'Monday':
            s_day = 0
        if session.day == 'Tuesday':
            s_day = 1
        if session.day == 'Wednesday':
            s_day = 2
        if session.day == 'Thursday':
            s_day = 3
        if session.day == 'Friday':
            s_day = 4
        if session.day == 'Saturday':
            s_day = 5
        if session.day == 'Sunday':
            s_day = 6
        t_day = today.weekday()
        local = localtime() + datetime.timedelta(hours=1)
        local = local.time()
        if s_day == t_day:
            if session.start_time <= local:
                start_day = today + datetime.timedelta(days=7)
            else:
                start_day = today
        if s_day > t_day:
            diff = s_day - t_day
            start_day = today + datetime.timedelta(days=diff)
        if s_day < t_day:
            diff = 7 - (t_day - s_day)
            start_day = today + datetime.timedelta(days=diff)
        start_day_to_add = start_day.strftime("%m/%d/%Y")
        choices.append((str(start_day), str(start_day_to_add)))
        for i in range(0, 5):
            start_day = start_day + datetime.timedelta(days=7)
            start_day_to_add = start_day.strftime("%m/%d/%Y")
            choices.append((str(start_day), str(start_day_to_add)))

        self.fields['Select_Sess'] = forms.CharField(label='Select a specific date:', widget=forms.Select(choices=choices))
