from django.db import models



class Campus(models.Model):
    build = models.CharField(max_length=255)
    # url = models.SlugField(max_length=100, unique=True)
    # def __str__(self):
    #     return self.build

class Classes(models.Model):
    room = models.ForeignKey(Campus, on_delete = models.CASCADE)
    number = models.CharField(max_length=22)

    # pass