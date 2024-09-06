from .models import ContactModel
from django import forms
class ContactForm(forms.ModelForm):
    class Meta:
        model=ContactModel
        fields='__all__'
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your name: '}),
            'Phone_number':forms.TextInput(attrs={'placeholder':'Enter your phone number '}),
            'gmail':forms.TextInput(attrs={'placeholder':'Enter your gmail'}),
            'password':forms.TextInput(attrs={'placeholder':'Enter your password'}),
            'text':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Say Anything','rows':9})
        }
        labels={
            'name':'Your Name: ',
            'Phone_number':'Your Phone Number: ',
            'gmail':'Your Gmail: ',
            'password':'Your Password: ',
            'text':'Your details: '
        }
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields['Phone_number'].initial='+8801'
    
    def clean_name(self):
        value=self.cleaned_data.get('name')
        n_o_w=value.split(' ')
        if len(n_o_w) > 3:
            self.add_error('name', 'name can have maximum 3 word')
        else:
            return value
