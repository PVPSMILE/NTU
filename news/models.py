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
class TypeOfRequest(models.Model):
    name = models.CharField("Name", max_length=100, default="Article")
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