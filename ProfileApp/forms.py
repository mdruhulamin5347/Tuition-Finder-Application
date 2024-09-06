from django import forms
from .models import UserProfile, TeacherProfile
from django.forms import CheckboxSelectMultiple

class UserProfileForm(forms.ModelForm):
    birth_date=forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model=UserProfile
        exclude=('user',)


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model=TeacherProfile
        exclude=('user',)
        widgets={
            'subject':CheckboxSelectMultiple(attrs={
                'multiple':True,
            }),
            'classin':CheckboxSelectMultiple(attrs={
                'multiple':True,
            })
        }
