from register.models import RegistrationModel
from django.forms import ModelForm
from django import forms 
from django.forms import ModelForm, TextInput,PasswordInput,CheckboxInput,Textarea,FileInput,NumberInput
class RegistrationForm(ModelForm):
    class Meta:
        model = RegistrationModel
        exclude = ('role',)
        fileds = ['last_name','first_name', 'email', 'password']
        widgets = {
            "last_name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name",
                "type": "text",
                "id": "Last_name",
                "name": "Last_name"
            }),
            "first_name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name",
                "type": "text",
                "id": "password"
            }),
            "email": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Email",
                "type": "text",
            }),
            "password": PasswordInput(render_value = True, attrs={
                "class": "form-control",
                "placeholder": "Password",
                "type": "password",
            }),
            
        }
class RepeatForm(forms.Form):
        repeat_password = forms.CharField(max_length=40, widget=TextInput(attrs={
        "placeholder": "Repeat password",
        "type": "password",
        "class": "r_password",
        "id":"r_password"
        }))
        