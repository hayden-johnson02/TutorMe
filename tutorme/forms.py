from django import forms

from tutorme.models import Profile


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
        exclude = {'email', 'is_tutor', 'is_student'}
        fields = {'first_name', 'last_name', 'bio'}


