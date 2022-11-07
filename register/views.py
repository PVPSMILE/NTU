from django.shortcuts import render
from register.forms import RegistrationForm, RepeatForm
from register.models import RegistrationModel
from django.shortcuts import redirect
# Create your views here.

def reg(request):
    if request.method == "POST":
        model = RegistrationModel.objects.all()
        form = RegistrationForm(request.POST)
        if form.is_valid():
                  form = form.save(commit=False)
                  form.role = "student"
                  form.save()
                  return redirect("/")
        else:
            print(False)
    form = RegistrationForm()
    return render(request, 'register/register.html', locals())

def login(request):
    
    return render(request, 'register/login.html', locals())
