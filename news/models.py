from django.db import models

class PublicationModel(models.Model):
    name = models.CharField("Name", max_length=100)
    discription = models.TextField("discription")
    author = models.CharField("author",max_length=100)
    url = models.SlugField(max_length=100) 