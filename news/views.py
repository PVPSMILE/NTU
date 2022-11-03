from django.shortcuts import render

def index(request):
    if 'Auth' not in request.session:
        request.session["Auth"] = False
        status ={
            "Auth": request.session["Auth"]
        }
        return render(request, 'base.html',locals())
    else:
        status = {
            "Auth": request.session["Auth"],
            "Name": request.session["Name"]
        }
        return render(request, 'base.html', locals())