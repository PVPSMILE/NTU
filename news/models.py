from django.db import models
import datetime
class Tags(models.Model):
    name = models.CharField("Name", max_length=100,default="gello")
    def __str__(self):
        return self.name
class Status(models.Model):
    name = models.CharField("Name", max_length=100,default="Processing")
    def __str__(self):
        return self.name
class StatusMessage(models.Model):
    name = models.CharField("Name", max_length=100, default="Processing")
    def __str__(self):
        return self.name
class StatusChat(models.Model):
    name = models.CharField("Name", max_length=100)
    def __str__(self):
        return self.name
class TypeOfRequest(models.Model):
    name = models.CharField("Name", max_length=100, default="Article")
    def __str__(self):
        return self.name
class TypeOfChat(models.Model):
    name = models.CharField("Name", max_length=100)
    def __str__(self):
        return self.name
class FullStateOfChat(models.Model):
    name = models.CharField("Name", max_length=100)
    def __str__(self):
        return self.name
class PublicationModel(models.Model):
    name = models.CharField("Name", max_length=100)
    title_image = models.ImageField(upload_to='news',default="default.jpg")
    discription = models.TextField("discription")
    author = models.ForeignKey("register.RegistrationModel",on_delete=models.CASCADE,null=True)
    date_of_create = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    time_of_create = models.TimeField(auto_now_add=True,auto_now=False,blank=True)
    date_of_update = models.DateField(auto_now=True,auto_now_add=False,blank=True)
    time_of_update = models.TimeField(auto_now=True,auto_now_add=False,blank=True)
    tags = models.ForeignKey(Tags,on_delete=models.CASCADE,default=0)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    type = models.ForeignKey(TypeOfRequest,on_delete=models.CASCADE,null=True)
    review = models.TextField("Review",blank=True,null=True)
class FriendModel(models.Model):
    surname = models.CharField("Last_Name",max_length=250)
    name = models.CharField("First_Name",max_length=250)
    email = models.EmailField("Email", max_length=100)
    friend = models.ForeignKey("register.RegistrationModel",on_delete=models.CASCADE,null=True)
    owner = models.ForeignKey("register.RegistrationModel",on_delete=models.CASCADE,null=True, related_name="getter")
class MessageModel(models.Model):
    room_name = models.CharField("Room Name",max_length=150)
    message = models.TextField("Message")
    owner = models.ForeignKey("register.RegistrationModel", on_delete=models.CASCADE, null=True, related_name="owner")
    date_of_create = models.DateField(auto_now_add=True,auto_now=False)
    time_of_create = models.TimeField(auto_now_add=True,auto_now=False)
    date_of_update = models.DateField(auto_now=True,auto_now_add=False)
    time_of_update = models.TimeField(auto_now=True,auto_now_add=False)
class ChatModel(models.Model):
    channel_name = models.CharField("Channel Name", max_length=300,null=True)
    room_name = models.CharField("Room Name", max_length=150)
    name = models.CharField("First Name", max_length=250,null=True)
    surname = models.CharField("Last Name", max_length=250,null=True)
    participant = models.ForeignKey("register.RegistrationModel", on_delete=models.CASCADE,null=True,related_name="participant")
    active = models.BooleanField("Active Chat",default=False)
    status = models.ForeignKey(StatusChat,on_delete=models.CASCADE,null=True)
    type_chat = models.ForeignKey(TypeOfChat,on_delete=models.CASCADE,null=True)
    full_state = models.ForeignKey(FullStateOfChat,on_delete=models.CASCADE,null=True)