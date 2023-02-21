from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from tutorme.models import Student, User


#class createStudentForm(UserCreationForm):

class StudentSignUpForm(ModelForm):

    class Meta:
        model = User
        exclude = ('is_tutor', 'is_student')
        fields = {'first_name', 'last_name', 'email'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
    }

