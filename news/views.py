import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render,redirect
from django.urls import reverse
from news.models import PublicationModel,Status,TypeOfRequest,FriendModel,MessageModel,ChatModel,StatusChat,FullStateOfChat
from register.models import RegistrationModel,Role
from django.contrib.postgres.search import SearchVector,SearchQuery,TrigramSimilarity
from news.forms import PublicationForm, AccountForm,ArticleForm,NewsForm
from django.db.models import Q
def get_last_room_name(request):
    chat = MessageModel.objects.filter(sender__email=request.session["Email"]).order_by("-date_of_update","-time_of_update")[0]
    return str(chat.room_name)
def index(request):
    if request.method == "POST":
        if request.POST.get("search"):
            query = SearchQuery(request.POST.get("search"),config='Russian',search_type='websearch')
            search_news = PublicationModel.objects.annotate(search=SearchVector("author","name","discription",config='Russian')).filter(search=query)
            search_similarity_name_news = PublicationModel.objects.annotate(similarity=TrigramSimilarity("name",request.POST.get("search"))).filter(similarity__gt=0.03).order_by('-similarity')
            search_similarity_discription_news = PublicationModel.objects.annotate(similarity=TrigramSimilarity("discription", request.POST.get("search"))).filter(similarity__gt=0.03).order_by('-similarity')
            search_similarity_author_news = PublicationModel.objects.annotate(similarity=TrigramSimilarity("author", request.POST.get("search"))).filter(similarity__gt=0.03).order_by('-similarity')
            return render(request, 'news/news.html', locals())
        if request.POST.get("filter"):
            filter = request.POST.getlist("filter")
            filters = PublicationModel.objects.filter(tags__name__in=filter)
            return render(request, 'news/news.html', locals())
    try:
        if request.session["Auth"]:
            news = PublicationModel.objects.filter(status__name="Accept").order_by("-date_of_update", "-time_of_update")
            response = render(request, 'news/news.html', locals())
            response.set_cookie("Email",request.session["Email"])
            return response
        else:
            news = PublicationModel.objects.filter(status__name="Accept").order_by("-date_of_update", "-time_of_update")
            return render(request, 'news/news.html', locals())
    except KeyError:
        news = PublicationModel.objects.filter(status__name="Accept").order_by("-date_of_update", "-time_of_update")
        return render(request, 'news/news.html', locals())
def detail(request,primary_key):
    if request.method == "POST":
        if request.POST.get("email"):
            number = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
            exist = ChatModel.objects.filter(room_name=number,participant__email=request.session["Email"]).exists()
            if exist:
                return redirect(reverse("news:chat"))
            else:
                if request.session["Email"] == request.POST.get("email"):
                    return redirect("/")
                else:
                    owner = RegistrationModel.objects.get(email=request.session["Email"])
                    guest = RegistrationModel.objects.get(email=request.POST.get("email"))
                    full =  FullStateOfChat.objects.get("Full")
                    empty = FullStateOfChat.objects.get("Clean")
                    disable = StatusChat.objects.get(name="Disable")
                    wait = StatusChat.objects.get(name="Wait")
                    chat1 = ChatModel(room_name=number, name=owner.first_name, surname=owner.last_name,participant=owner, active=True, status=wait, full_state=empty)
                    chat2 = ChatModel(room_name=number, name=guest.first_name, surname=guest.last_name,participant=guest, active=False, status=disable, full_state=empty)
                    chat1.save()
                    chat2.save()
                    return redirect(reverse("news:chats"))
    news = PublicationModel.objects.get(pk=primary_key)
    return render(request, 'news/detail_news.html', locals())
def admin_request_page(request):
    if request.session["Role"] != "Admin":
        return redirect("/")
    else:
        news = PublicationModel.objects.filter(status__name="Processing")
        accounts = RegistrationModel.objects.filter(status__name="Processing")
        return render(request, 'news/request.html', locals())
def admin_request_detail_article_page(request,primary_key):
    if request.session["Role"] != "Admin":
        return redirect("/")
    else:
        news = PublicationModel.objects.get(pk=primary_key)
        if request.method == "POST":
            if request.POST.get('Accept'):
                 b = Status.objects.get(name="Accept")
                 PublicationModel.objects.filter(id=primary_key).update(status=b.id)
                 return redirect(reverse("news:request"))
            else:
                forms = PublicationForm(request.POST,instance=news)
                if forms.is_valid():
                    form = forms.save(commit=False)
                    b = Status.objects.get(name="Refuse")
                    form.status_id = b.id
                    form.save()
                    return redirect(reverse("news:request"))
        forms = PublicationForm(instance=news)
        return render(request, 'news/datail_article_request.html', locals())
def admin_request_detail_account_page(request,primary_key):
    if request.session["Role"] != "Admin":
        return redirect("/")
    else:
        accounts = RegistrationModel.objects.get(pk=primary_key)
        if request.method == "POST":
            data = RegistrationModel.objects.filter(id=primary_key)[0]
            if request.POST.get('Accept'):
                 status = Status.objects.get(name="Accept")
                 role = Role.objects.get(name="Moderator")
                 RegistrationModel.objects.filter(id=primary_key).update(status=status.id,role=role.id)
                 send_raise_level_account_email(data.email)
                 return redirect(reverse("news:request"))
            else:
                forms = AccountForm(request.POST)
                if forms.is_valid():
                    letter = forms.cleaned_data["reason"]
                    send_recomandation_email(data.email,letter)
                    return redirect(reverse("news:request"))
        form = AccountForm()
        return render(request, 'news/detail_account_request.html', locals())
def articls_page(request,pk):
    if request.session["Role"] != "Moderator" and request.session["Role"] != "Admin":
        return redirect("/")
    else:
        articles = PublicationModel.objects.filter(author=pk)
        return render(request, 'news/articls.html', locals())
def detail_article_page(request,pk):
    if request.session["Role"] != "Moderator" and request.session["Role"] != "Admin":
        return redirect("/")
    else:
        article = PublicationModel.objects.get(id=pk)
        if request.method == "POST":
            if request.POST.get("delete"):
                article.delete()
                return redirect(reverse("news:list_articls", args=(request.session.get("id"),)))
            else:
                forms = ArticleForm(request.POST,request.FILES,instance=article)
                if forms.is_valid():
                    form = forms.save(commit=False)
                    status = Status.objects.get(name="Processing")
                    form.status_id = status.id
                    form.save()
                    return redirect(reverse("news:list_articls",args=(request.session.get("id"),)))
        try:
            len_review = len(article.review)
        except TypeError:
            len_review = 0
        forms = ArticleForm(instance=article)
        return render(request, 'news/detail_article_moderator.html', locals())
def detail_create_article_page(request):
    if request.session["Role"] != "Moderator" and request.session["Role"] != "Admin":
        return redirect("/")
    else:
        if request.method == "POST":
            forms = ArticleForm(request.POST,request.FILES)
            if forms.is_valid():
                form = forms.save(commit=False)
                status = Status.objects.get(name="Processing")
                status2 = Status.objects.get(name="Accept")
                author = RegistrationModel.objects.get(id=int(request.session.get("id")))
                type = TypeOfRequest.objects.get(name="Article")
                if request.session["Role"] == "Admin":
                    form.status_id = status2.id
                else:
                    form.status_id = status.id
                form.author_id = author.id
                form.type_id = type.id
                form.save()
                return redirect(reverse("news:list_articls", args=(request.session.get("id"),)))
        forms = ArticleForm()
        return render(request, 'news/detail_create_article_moderator.html', locals())
def all_article_page(request):
    if request.session["Role"] != "Admin":
        return redirect("/")
    else:
        if request.method == "POST":
            if request.POST.get("filter"):
                filters = PublicationModel.objects.filter(status__name__in=request.POST.getlist("filter"))
                return render(request, 'news/all_article.html', locals())
        news = PublicationModel.objects.all()
        return render(request,'news/all_article.html',locals())
def all_article_detail_page(request,pk):
    if request.session["Role"] != "Admin":
        return redirect("/")
    else:
        new = PublicationModel.objects.get(id=pk)
        if request.method == "POST":
            forms = NewsForm(request.POST,instance=new)
            if forms.is_valid():
                forms.save()
                return redirect(reverse("news:all_news"))
        forms = NewsForm(instance=new)
        return render(request, 'news/detail_article.html', locals())
def chats(request):
    my_chats = ChatModel.objects.filter(Q(status__name="Active" ,participant__email=request.session["Email"],active=True)|Q(status__name="Wait",participant__email=request.session["Email"],active=True))
    chats,last_messages = get_chat_list(my_chats,request)
    friends = FriendModel.objects.filter(owner__email=request.session["Email"])
    print(friends)
    return render(request, 'news/chats.html', locals())
def chat(request,room_name):
    exists = ChatModel.objects.filter(participant__email=request.session["Email"],room_name=room_name).exists()
    if exists:
        chat = ChatModel.objects.get(participant__email=request.session["Email"],room_name=room_name)
        datas = ChatModel.objects.filter(room_name=room_name).exclude(participant__email=request.session["Email"])
        data = ChatModel.objects.filter(room_name=room_name).exclude(participant__email=request.session["Email"])[0]
        if chat.status.name == "Disable":
            wait = StatusChat.objects.get(name="Wait")
            ChatModel.objects.filter(participant__email=request.session["Email"],room_name=room_name).update(status=wait.id,active=True)
        my_chats = ChatModel.objects.filter(Q(status__name="Active",participant__email=request.session["Email"],active=True) | Q(status__name="Wait",participant__email=request.session["Email"],active=True))
        chats,last_messages = get_chat_list(my_chats, request)
        messages = MessageModel.objects.filter(room_name=room_name)
        friends = FriendModel.objects.filter(owner__email=request.session["Email"])
        return render(request, 'news/chat.html', locals())
    else:
        return redirect(reverse("news:chats"))
def friends_page(request):
    if request.method == "POST":
        if request.POST.get("Find"):
            friend = RegistrationModel.objects.get(email=request.POST.get("Find"))
            return render(request, 'news/friends.html', locals())
    friends = FriendModel.objects.filter(owner__email=request.session["Email"])
    return render(request, 'news/friends.html', locals())
def friend_detail_page(request,email):
    friend = RegistrationModel.objects.get(email=email)
    if request.method == "POST":
        if request.POST.get("Chat"):
            number = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
            owner = RegistrationModel.objects.get(email=request.session["Email"])
            guest = RegistrationModel.objects.get(email=request.POST.get("Chat"))
            full = FullStateOfChat.objects.get(name="Full")
            empty = FullStateOfChat.objects.get(name="Clean")
            disable = StatusChat.objects.get(name="Disable")
            wait = StatusChat.objects.get(name="Wait")
            chat1 = ChatModel(room_name=number, name=owner.first_name,surname=owner.last_name,participant=owner, active=True, status=wait, full_state=empty)
            chat2 = ChatModel(room_name=number, name=guest.first_name,surname=guest.last_name,participant=guest, active=False, status=disable, full_state=empty)
            chat1.save()
            chat2.save()
            return redirect(reverse("news:chats"))
        elif request.POST.get("Add"):
            owner = RegistrationModel.objects.get(email=request.session["Email"])
            friend = FriendModel(friend=friend,owner=owner,email=friend.email,name=friend.first_name,surname=friend.last_name)
            friend.save()
    return render(request, 'news/detail_friend.html', locals())
def get_chat_list(chats,request):
    rooms = []
    last_messages = []
    for chat in chats:
        if chat.full_state.name == "Clean":
            chat = ChatModel.objects.filter(room_name=chat.room_name).exclude(participant__email=request.session["Email"])
            rooms.append(chat)
        else:
            message = MessageModel.objects.filter(room_name=chat.room_name).values().last()
            chat = ChatModel.objects.filter(Q(room_name=chat.room_name, status__name="Active", active=True,full_state__name="Full") | Q(room_name=chat.room_name,status__name="Wait",active=True,full_state__name="Full")).exclude(participant__email=request.session["Email"])
            rooms.append(chat)
            last_messages.append(message)
    return rooms, last_messages
def send_recomandation_email(email,letter):
    my_email = "buyahh11@gmail.com"
    to = email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = my_email
    msg['To'] = to
    string_text = letter
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
def send_raise_level_account_email(email):
    my_email = "buyahh11@gmail.com"
    to = email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = my_email
    msg['To'] = to
    string_text = "Congratulations! You get access to rights of Moderator.Now, you can create articles and a lot of other things! If you have any questions,you are able to write in support. Good luck!! "
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

