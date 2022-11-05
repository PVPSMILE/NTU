import smtplib
import random
import string
from django.shortcuts import render
from register.forms import RegistrationForm,CodeForm,AuthorizationForm,SetUpDataForm
from register.models import RegistrationModel, Role
from django.shortcuts import redirect
from django.urls import reverse
def reg(request):
    if request.method == "POST":
        model = Role.objects.filter(name="Student")[0]
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
                  form = forms.save(commit=False)
                  form.role_id = model.id
                  form.save()
                  code = send_email(forms.cleaned_data["email"],forms.cleaned_data["first_name"])
                  request.session["Code"] = code
                  request.session["Name"] = forms.cleaned_data["first_name"]
                  request.session["Email"] = forms.cleaned_data["email"]
                  return redirect(reverse("register:code"))
        else:
            return render(request, 'register/index.html', locals())
    forms = RegistrationForm()
    return render(request, 'register/index.html',locals())
def send_code(request):
    if request.method == "POST":
        if request.POST.get("req"):
            code = send_email(request.session["Email"], request.session["Name"])
            request.session["Code"] = code
        else:
            forms = CodeForm(request, request.POST)
            if forms.is_valid():
                data = RegistrationModel.objects.filter(first_name=request.session["Name"],
                                                        email=request.session["Email"]).update(is_active=True)
                request.session["Auth"] = True
                return redirect("/")
            else:
                return render(request, 'register/code.html', locals())
    forms = CodeForm(request)
    return render(request, 'register/code.html',locals())
def auth(request):
    if request.method == "POST":
        forms = AuthorizationForm(request.POST)
        if forms.is_valid():
            data = RegistrationModel.objects.filter(password=forms.cleaned_data["password"],email=forms.cleaned_data["email"])[0]
            request.session["Name"] = data.first_name
            request.session["Email"] = forms.cleaned_data["email"]
            request.session["Auth"] = data.is_active
            return redirect("/")
        else:
            return render(request, 'register/auth.html', locals())
    forms = AuthorizationForm()
    return render(request, 'register/auth.html', locals())
def sing_out(request):
    request.session["Auth"] = False
    return redirect("/")
def setup_data(request):
    data = RegistrationModel.objects.filter(email=request.session["Email"])[0]
    if request.method == "POST":
        if request.POST.get("delete"):
            RegistrationModel.objects.filter(email=request.session["Email"]).delete()
            del request.session["Auth"]
            del request.session["Name"]
            del request.session["Email"]
            return redirect("/")
        else:
            forms = SetUpDataForm(request.POST,instance=data)
            if forms.is_valid():
                forms.save()
                return redirect(reverse("register:update"))
    forms = SetUpDataForm(instance=data)
    return render(request,'register/update_data.html',locals())
def send_email(email,name):
    S = 6  # number of characters in the string.
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    code = ran
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('buyahh11@gmail.com', 'shdjnaonlixhfgfz')

    try:
        server.sendmail('buyahh11@gmail.com',email,              'Hi %s,'
                                                                 'We are happy you signed up.To start exploring,please confirm your email address.'
                                                                 'Your code is %s.' % (name, code))
    except:
        print('An error occurred when trying to send an email')

    server.quit()
    return code
