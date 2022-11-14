from django.shortcuts import render
from news.models import PublicationModel
from django.contrib.postgres.search import SearchVector,SearchQuery,TrigramSimilarity
def index(request):
    if request.method == "POST":
        if request.POST.get("search"):
            query = SearchQuery(request.POST.get("search"),config='Russian',search_type='websearch')
            search_news = PublicationModel.objects.annotate(search=SearchVector("author","name","discription",config='Russian')).filter(search=query)
            search_similarity_name_news = PublicationModel.objects.annotate(similarity=TrigramSimilarity("name",request.POST.get("search"))).filter(similarity__gt=0.03).order_by('-similarity')
            search_similarity_discription_news = PublicationModel.objects.annotate(similarity=TrigramSimilarity("discription", request.POST.get("search"))).filter(similarity__gt=0.03).order_by('-similarity')
            search_similarity_author_news = PublicationModel.objects.annotate(similarity=TrigramSimilarity("author", request.POST.get("search"))).filter(similarity__gt=0.03).order_by('-similarity')
            print(search_similarity_name_news)
            print(search_similarity_discription_news)
            print(search_similarity_author_news)
            print(search_news)
            return render(request, 'news/news.html', locals())
        if request.POST.get("filter"):
            filter = request.POST.getlist("filter")
            filters = PublicationModel.objects.filter(tags__name__in=filter)
            return render(request, 'news/news.html', locals())
    news = PublicationModel.objects.all()
    return render(request, 'news/news.html', locals())