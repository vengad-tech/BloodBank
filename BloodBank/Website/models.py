from django.db import models
#from django.core.management.validation import max_length


# Create your models here.
class RegisteredUsers(models.Model):
    name = models.CharField(max_length=30)
    email=models.EmailField(primary_key=True)
    pswd = models.CharField(max_length=30)
    bloodgroup = models.CharField(max_length=4 )
    mobile = models.IntegerField(max_length=10)
    sex = models.CharField(max_length=6)
    dob = models.DateField()
    dolbd = models.DateField()
    city = models.CharField(max_length=20)
    hidemob = models.CharField(max_length=3)
    
class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.IntegerField(max_length=10)
    value = models.TextField(max_length=300)