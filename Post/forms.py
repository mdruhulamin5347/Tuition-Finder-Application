from django import forms
from .models import PostModel, PhotoAddModel
from django.forms import CheckboxSelectMultiple
# from .fields import ListTextWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        exclude = ['user', 'slug', 'created_at', 'likes', 'views']
        widgets = {
            'subject': CheckboxSelectMultiple(attrs={
                'multiple': True,
            }),
            'classin': CheckboxSelectMultiple(attrs={
                'multiple': True,
            }),
        }

    # def __init__(self, *args, **kwargs):
    #     _district_set = kwargs.pop('district_set', None)
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['district'].widget = ListTextWidget(data_list=_district_set, name='district')

class PhotoAddForm(forms.ModelForm):
    class Meta:
        model = PhotoAddModel
        fields = ['image']
