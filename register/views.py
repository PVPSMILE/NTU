import os
import smtplib
import random
import string
import codecs
import django
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render
from register.forms import RegistrationForm,CodeForm,AuthorizationForm,SetUpDataForm
from register.models import RegistrationModel, Role
from news.models import TypeOfRequest,Status
from django.shortcuts import redirect
from django.urls import reverse
def reg(request):
    role = Role.objects.filter(name="Student")[0]
    type = TypeOfRequest.objects.filter(name="Account")[0]
    status = Status.objects.filter(name="Processing")[0]
    if request.method == "POST":
        forms = RegistrationForm(request.POST)
        if request.session["Role"] == "Student":
            if forms.is_valid():
                      form = forms.save(commit=False)
                      form.role_id = role.id
                      form.save()
                      code = send_email(forms.cleaned_data["email"],forms.cleaned_data["first_name"])
                      request.session["Code"] = code
                      request.session["Name"] = forms.cleaned_data["first_name"]
                      request.session["Surname"] = forms.cleaned_data["last_name"]
                      request.session["Email"] = forms.cleaned_data["email"]
                      return redirect(reverse("register:code"))
            else:
                return render(request, 'register/register.html', locals())
        elif request.session["Role"] == "Moderator":
            if forms.is_valid():
                      form = forms.save(commit=False)
                      form.role_id = role.id
                      form.type_id = type.id
                      form.status_id = status.id
                      form.save()
                      code = send_email(forms.cleaned_data["email"],forms.cleaned_data["first_name"])
                      request.session["Code"] = code
                      request.session["Name"] = forms.cleaned_data["first_name"]
                      request.session["Surname"] = forms.cleaned_data["last_name"]
                      request.session["Email"] = forms.cleaned_data["email"]
                      return redirect(reverse("register:code"))
            else:
                return render(request, 'register/register.html', locals())
    forms = RegistrationForm()
    return render(request, 'register/register.html',locals())
def send_code(request):
    if request.method == "POST":
        if request.POST.get("req"):
            code = send_email(request.session["Email"], request.session["Name"])
            request.session["Code"] = code
        else:
            forms = CodeForm(request, request.POST)
            if forms.is_valid():
                data = RegistrationModel.objects.filter(first_name=request.session["Name"], email=request.session["Email"])[0]
                request.session["Auth"] = True
                request.session["Path_Image"] = "/media" + "/profile/" + data.photo.name
                request.session["id"] = data.id
                send_alert_email(request.session["Email"], request.session["Name"])
                return redirect("/")
            else:
                return render(request, 'register/codes.html', locals())
    forms = CodeForm(request)
    return render(request, 'register/codes.html', locals())
def login(request):
    if request.method == "POST":
        forms = AuthorizationForm(request.POST)
        if forms.is_valid():
            data = RegistrationModel.objects.filter(password=forms.cleaned_data["password"],email=forms.cleaned_data["email"])[0]
            request.session["Name"] = data.first_name
            request.session["Email"] = forms.cleaned_data["email"]
            request.session["Auth"] = True
            request.session["id"] = data.id
            if data.photo.name == "depositphotos_199564354-stock-illustration-creative-vector-illustration-of-default.jpg":
                    request.session["Path_Image"] = "/media" + "/profile/" + data.photo.name
            else:
                request.session["Path_Image"] = "/media/" + data.photo.name
            request.session["Role"] = data.role.name
            return redirect("/")
        else:
            return render(request, 'register/login.html', locals())
    forms = AuthorizationForm()
    return render(request, 'register/login.html', locals())
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
            forms = SetUpDataForm(request.POST,request.FILES,instance=data)
            if forms.is_valid():
                request.session["Name"] = forms.cleaned_data["first_name"]
                request.session["Email"] = forms.cleaned_data["email"]
                try:
                    name = str(request.FILES["photo"]).replace(" ","_")
                except django.utils.datastructures.MultiValueDictKeyError:
                    forms.save()
                    return redirect(reverse("register:update"))
                else:
                    request.session["Path_Image"] = os.path.join("/media/profile/", name)
                    forms.save()
                    return redirect(reverse("register:update"))
    forms = SetUpDataForm(instance=data)
    return render(request,'register/settings.html',locals())
def role(request):
    if request.method == "POST":
        if request.POST.get("Role") == "Student":
            request.session["Role"] = "Student"
            return redirect(reverse("register:reg"))
        elif request.POST.get("Role") == "Moderator":
            request.session["Role"] = "Moderator"
            return redirect(reverse("register:reg"))
    return render(request,'register/role.html',locals())
def send_email(email,name):
    my_email = "buyahh11@gmail.com"
    to = email
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = my_email
    msg['To'] = to
    current_directory = os.path.dirname(os.path.realpath(__file__))
    with codecs.open(current_directory+"//"+"index.html",encoding='utf-8', mode='r') as html_email:
        text_html = html_email.read()
        html_email.close()
        text_with_name = text_html.replace("Name",name)
        S = 6  # number of characters in the string.
        # call random.choices() string module to find the string in Uppercase + numeric data.
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        code = ran
        string_text = 'Hi %s,''We are happy you signed up.To start exploring,please confirm your email address.''Your code is %s' % (name, code)
        ready_html_text = text_with_name.replace("Code",code)
        part1 = MIMEText(string_text, 'plain')
        part2 = MIMEText(ready_html_text, 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('buyahh11@gmail.com', 'shdjnaonlixhfgfz')
        try:
            server.sendmail(my_email,email,msg.as_string())
        except:
            print('An error occurred when trying to send an email')
        server.quit()
        return code
def send_alert_email(email,name):
    my_email = "buyahh11@gmail.com"
    to = email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = my_email
    msg['To'] = to
    string_text = '%s,''We wanted to let you know that we need to make a few extra checks on our side to verify your identity. This means it will take a little longer to get you verified and use privelage of Moderator.' 'Right now you dont need to do anything. Our support team may get in contact if there any extra information we need.' % (name)
    part1 = MIMEText(string_text, 'plain')
    msg.attach(part1)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('buyahh11@gmail.com', 'shdjnaonlixhfgfz')
    try:
        server.sendmail(my_email,email,msg.as_string())
    except:
        print('An error occurred when trying to send an email')
    server.quit()