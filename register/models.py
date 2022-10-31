from django.db import models
class RegistrationModel(models.Model):
    last_name = models.CharField("Last_Name",max_length=250)
    first_name = models.CharField("First_Name",max_length=250)
    email = models.EmailField("Email", max_length=100)
    password = models.CharField("Password",max_length=250)
    role = models.CharField("Role",max_length=250)
    def __str__(self):
        return  self.last_name

    
