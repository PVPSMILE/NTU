from django.db import models
import datetime
class Tags(models.Model):
    name = models.CharField("Name", max_length=100,default="gello")
    def __str__(self):
        return self.name
class PublicationModel(models.Model):
    name = models.CharField("Name", max_length=100)
    # title_image = models.ImageField("Title image",)
    discription = models.TextField("discription")
    author = models.CharField("author",max_length=100)
    date_of_create = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    time_of_create = models.TimeField(auto_now_add=True,auto_now=False,blank=True)
    date_of_update = models.DateField(auto_now=True,auto_now_add=False,blank=True)
    time_of_update = models.TimeField(auto_now=True,auto_now_add=False,blank=True)
    tags = models.ForeignKey(Tags,on_delete=models.CASCADE,default=0)
