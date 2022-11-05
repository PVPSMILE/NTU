from register.models import RegistrationModel
from django.forms import ModelForm
from django import forms 
from django.forms import ModelForm, TextInput,PasswordInput,CheckboxInput,Textarea,FileInput,NumberInput
from django.contrib.sessions.backends.db import SessionStore
class CodeForm(forms.Form):
    def __init__(self,request,*args, **kwargs):
        super(CodeForm, self).__init__(*args, **kwargs)
        self.code = request.session["Code"]
    code = forms.CharField(max_length=6,widget=TextInput(attrs={
        "placeholder": "Enter code",
        "type":"text",
        "class": "form-control",
        "id": "code",
        "style": "width: 166px; height: 61px;"
    }))
    def clean(self):
        super(CodeForm, self).clean()
        code = self.cleaned_data["code"]
        if len(code) != 6:
            self._errors['code'] = self.error_class(['Invalid code.Try again.'])
        elif (self.code).upper() != (self.cleaned_data["code"]).upper():
            self._errors['code'] = self.error_class(['Invalid code.Try again.'])
class RegistrationForm(ModelForm):
    def __int__(self):
        super(RegistrationForm, self).__init__().is_valid()
    repeat_password = forms.CharField(max_length=110, widget=PasswordInput(attrs={
        "placeholder": "Repeat password",
        "type": "password",
        "class": "form-control",
        "id": "r_password"
    }))
    password = forms.CharField(max_length=110, widget=PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password",
        "type": "password",
    }))
    class Meta:
        model = RegistrationModel
        exclude = ('role','is_active')
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
            
        }
    def clean(self):
        password= self.cleaned_data["password"]
        repeat_password = self.cleaned_data["repeat_password"]
        try:
            exist_email = RegistrationModel.objects.filter(email=self.cleaned_data["email"]).exists()
        except KeyError:
            self._errors["email"] = self.error_class(["Invalid email. Have you made account?"])
        else:
            if password != repeat_password:
                self._errors['repeat_password'] = self.error_class(['Password does not match.'])
            if exist_email:
                self._errors["email"] = self.error_class(['This email already in use. Please enter another'])
        return self.cleaned_data


class AuthorizationForm(ModelForm):
    password = forms.CharField(max_length=110, widget=PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password",
        "type": "password",
    }))
    class Meta:
        model = RegistrationModel
        exclude = ('role', 'is_active','last_name', 'first_name')
        fileds = ['email', 'password']
        widgets = {
            "email": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Email",
                "type": "text",
            }),

        }
    def clean(self):
        super(AuthorizationForm,self).clean()
        try:
            exist_account = RegistrationModel.objects.filter(email=self.cleaned_data["email"],password=self.cleaned_data["password"]).exists()
        except KeyError:
            self._errors["email"] = self.error_class(["Invalid email. Have you made account?"])
        else:
            if not exist_account:
                self._errors["password"] = self.error_class(["Invalid data. Have you made account?"])


class SetUpDataForm(ModelForm):
    password = forms.CharField(max_length=110,widget=PasswordInput(render_value=True, attrs={
        "class": "form-control",
        "placeholder": "Password",
        "type": "password",
    }))
    class Meta:
        model = RegistrationModel
        exclude = ('role', 'is_active')
        fileds = ['last_name', 'first_name', 'email', 'password']
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

        }
