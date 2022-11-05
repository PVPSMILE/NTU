from django.shortcuts import render
from news.models import PublicationModel
from django.db.models import Q
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse
def index(request):
    if request.method == "POST":
        if request.POST.get("search"):
            searches = PublicationModel.objects.filter(name__icontains=request.POST.get("search"))
            if len(searches) != 0:
                return render(request, 'news/search_news.html', locals())
            else:
                searches = PublicationModel.objects.filter(discription__icontains=request.POST.get("search"))
                if len(searches) != 0:
                    return render(request, 'news/search_news.html', locals())
                else:
                    searches = PublicationModel.objects.filter(author__icontains=request.POST.get("search"))
                    if len(searches) != 0:
                        return render(request, 'news/search_news.html', locals())
                    else:
                        return render(request, 'news/search_news.html', locals())
        elif request.POST.get("filter"):
            filter = request.POST.getlist("filter")
            filters = PublicationModel.objects.filter(tags__name__in=filter)
            return render(request, 'news/search_news.html', locals())
    searches = PublicationModel.objects.all()
    return render(request, 'news/search_news.html', locals())