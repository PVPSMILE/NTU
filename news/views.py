from django.shortcuts import render
from news.models import PublicationModel
from django.db.models import Q
def index(request):
    if request.method == "POST":
        if request.POST.get("search"):
            searches = PublicationModel.objects.filter(Q(name__icontains=request.POST.get("search")) | Q(discription__icontains=request.POST.get("search")) | Q(author__icontains=request.POST.get("search")))
            return render(request, 'news/get_data_news.html', locals())
    return render(request, 'news/search_news.html', locals())