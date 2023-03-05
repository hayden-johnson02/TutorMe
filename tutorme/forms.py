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
        exclude = {'is_tutor', 'is_student'}
        fields = {'first_name', 'last_name', 'email', 'bio'}

        # https://www.youtube.com/watch?v=6-XXvUENY_8 Styling
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'fname', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'lname', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'readonly class': 'form-control', 'id': 'email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-height: 300px;',
                                         'placeholder': 'Write some information about yourself!'}),
        }
