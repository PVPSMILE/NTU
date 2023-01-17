import json
import random
import string
from channels.generic.websocket import WebsocketConsumer,SyncConsumer
from asgiref.sync import async_to_sync
from news.models import ChatModel,MessageModel,StatusChat,FullStateOfChat,FriendModel
from register.models import RegistrationModel
import string
from django.db.models import Q
from django.contrib.postgres.search import SearchVector,SearchQuery,TrigramSimilarity
class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.name_channel = self.channel_name
            self.list_room_notofication = self.get_list_rooms(self.room_name)
            self.list_room_notofication.append(self.room_name)
            async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
            self.accept()
    def websocket_disconnect(self, message):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
    def websocket_receive(self, message):
        status = json.loads(message["text"])
        print("ChatSocket")
        print(status)
        if status["status"] == "send":
            state = self.check_state_chat()
            if state == "Clean":
                self.update_state_chat()
            self.save_message(status["message"],status["email"],self.room_name)
            for room in self.list_room_notofication:
                async_to_sync(self.channel_layer.group_send)(room, {"type": "send_message", "text": status})
        elif status["status"] == "add_friend":
            self.add_friends(status["friend_email"])
            self.update_status_chat()
        elif status["status"] == "connect":
            pass
    def send_message(self,event):
        message = event["text"]
        # Send message to WebSocket
        self.send(json.dumps({"message": message}))
    def save_message(self,message,email,room):
        owner = RegistrationModel.objects.get(email=email)
        message = MessageModel(room_name=room,message=message,owner=owner)
        message.save()
    def get_list_rooms(self,room_name):
        rooms = ChatModel.objects.filter(room_name=str(room_name))
        channels = []
        for room in rooms:
            channels.append(str(room.participant.email).replace("@", ""))
        return channels
    def check_state_chat(self):
        status = ChatModel.objects.get(room_name=self.room_name,participant__email=self.scope["session"]["Email"])
        return status.full_state.name
    def update_state_chat(self):
        clean = FullStateOfChat.objects.get(name="Full")
        ChatModel.objects.filter(room_name=self.room_name, participant__email=self.scope["session"]["Email"]).update(full_state=clean)
    def add_friends(self,email):
        owner = RegistrationModel.objects.get(email=self.scope["session"]["Email"])
        person_who_friend = RegistrationModel.objects.get(email=email)
        friend = FriendModel(surname=person_who_friend.last_name,name=person_who_friend.first_name,email=person_who_friend.email,friend=person_who_friend,owner=owner)
        friend.save()
    def update_status_chat(self):
        active = StatusChat.objects.get(name="Active")
        ChatModel.objects.filter(room_name=self.room_name).exclude(participant__email=self.scope["session"]["Email"]).update(status=active)
class NotificationConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        self.room_group_name = str(self.scope["session"]["Email"]).replace("@", "")
        self.name_channel = self.channel_name
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
    def websocket_disconnect(self, message):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
    def websocket_receive(self, message):
        status = json.loads(message["text"])
        print("NotificationSocket")
        print(status)
        if status["status"] == "connect":
            pass
        elif status["status"] == "search_chat":
            rooms,last_messages = self.search_chat(status["email"],status["value"])
            status["rooms"] = rooms
            status["last_messages"] = last_messages
            status["status"] = "get_chat"
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "send_message", "text": status})
        elif status["status"] == "get_list_chats":
            rooms,last_messages = self.return_all_chat_list()
            status["rooms"] = rooms
            status["last_messages"] = last_messages
            status["status"] = "list_chat"
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "send_message", "text": status})
        elif status["status"] == "search_friend":
            friends = self.search_friend(status["email"],status["value"])
            status["friends"] = friends
            status["status"] = "get_friend"
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "send_message", "text": status})
        elif status["status"] == "get_list_friends":
            friends = self.get_list_friends()
            status["friends"] = friends
            status["status"] = "list_friend"
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "send_message", "text": status})
        elif status["status"] == "check":
            exists = self.check_active_chat_exist(status["room_name"])
            if exists:
                status["status"] = "add_message_note"
                async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "send_message", "text": status})
            else:
                status["status"] = "add_chat"
                exists = self.check_disable_chat_exist(status["room_name"])
                if exists:
                    self.update_state_chat(status["room_name"])
                async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "send_message", "text": status})
    def send_message(self, event):
            message = event["text"]
            self.send(json.dumps({"message": message}))
    def update_state_chat(self,room_name):
        wait = StatusChat.objects.get(name="Wait")
        full = FullStateOfChat.objects.get(name="Full")
        ChatModel.objects.filter(room_name=room_name, participant__email=self.scope["session"]["Email"],active=False).update(active=True,status=wait,full_state=full)
    def check_disable_chat_exist(self,room_name):
        exist = ChatModel.objects.filter(room_name=room_name, participant__email=self.scope["session"]["Email"],active=False).exists()
        return exist
    def check_active_chat_exist(self, room_name):
        exist = ChatModel.objects.filter(room_name=room_name, participant__email=self.scope["session"]["Email"],active=True).exists()
        return exist
    def search_chat(self,email,value):
        chats = ChatModel.objects.filter(participant__email=email)
        rooms = []
        last_messages = []
        for chat in chats:
                messages = MessageModel.objects.filter(room_name=chat.room_name).values().last()
                chats = ChatModel.objects.annotate(similarity=TrigramSimilarity("surname",value)).filter(room_name=chat.room_name,similarity__gt=0.09).values().exclude(participant__email=email)
                if len(chats) > 0:
                    for chat in chats:
                        rooms.append(chat)
                try:
                    if len(messages) > 0:
                        for message in messages:
                            last_messages.append(message)
                except TypeError:
                    pass
        return rooms,last_messages
    def search_friend(self, email, value):
        friends = []
        friendss = FriendModel.objects.annotate(similarity=TrigramSimilarity("surname", value)).filter(owner__email=email,similarity__gt=0.09).values()
        for friend in friendss:
            friends.append(friend)
        return friends
    def get_list_friends(self):
        friends = []
        friendss = FriendModel.objects.filter(owner__email=self.scope["session"]["Email"]).values()
        for friend in friendss:
            friends.append(friend)
        return friends
    def return_all_chat_list(self):
            chats = ChatModel.objects.filter(Q(status__name="Active", participant__email=self.scope["session"]["Email"], active=True) | Q(status__name="Wait",participant__email=self.scope["session"]["Email"],active=True))
            rooms = []
            last_messages = []
            for chat in chats:
                if chat.full_state.name == "Clean":
                    chatss = ChatModel.objects.filter(room_name=chat.room_name).values().exclude(participant__email=self.scope["session"]["Email"])
                    for chat in chatss:
                        rooms.append(chat)
                else:
                    messages = MessageModel.objects.filter(room_name=chat.room_name).values().last()
                    chatss = ChatModel.objects.filter(Q(room_name=chat.room_name, status__name="Active", active=True, full_state__name="Full") | Q(room_name=chat.room_name, status__name="Wait", active=True,full_state__name="Full")).values().exclude(participant__email=self.scope["session"]["Email"])
                    for chat in chatss:
                        rooms.append(chat)
                    for message in messages:
                        last_messages.append(message)
            return rooms,last_messages
        # chats = ChatModel.objects.annotate(similarity=TrigramSimilarity("participant__email",)).filter(similarity__gt=0.03)
