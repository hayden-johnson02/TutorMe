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

        # https://stackoverflow.com/questions/350799/how-does-django-know-the-order-to-render-form-fields
        field_order = ['first_name', 'last_name', 'email', 'bio']

        # https://forum.djangoproject.com/t/change-label-of-a-field-in-a-form/14227
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'bio': 'Biography',
        }

        # https://www.youtube.com/watch?v=6-XXvUENY_8 Styling
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'readonly class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-height: 300px;',
                                         'placeholder': 'Write some information about yourself!'}),
        }
