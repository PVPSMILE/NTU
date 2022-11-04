from django.shortcuts import render
from nav.models import Campus,Classes
def nav(request):
        campuses = Campus.objects.all()
        classes = Campus.objects.all()
        data = {
            "campuses": campuses,
            "classes": classes,
        }
        return render(request, 'nav/navig.html' ,locals())


