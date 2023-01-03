from django.db import models
class Role(models.Model):
    name = models.CharField("Name of role",max_length=30)
    description = models.TextField("Description")
    def __str__(self):
        return self.name
class RegistrationModel(models.Model):
    last_name = models.CharField("Last_Name",max_length=250)
    first_name = models.CharField("First_Name",max_length=250)
    email = models.EmailField("Email", max_length=100)
    password = models.CharField("Password",max_length=250)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return  self.last_name

    
