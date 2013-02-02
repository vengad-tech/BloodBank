from django.db import models
#from django.core.management.validation import max_length


# Create your models here.
class RegisteredUsers(models.Model):
    name = models.CharField(max_length=30)
    email=models.EmailField(primary_key=True)
    pswd = models.CharField(max_length=30)
    bloodgroup = models.CharField(max_length=4 )
    mobile = models.CharField(max_length=10)
    sex = models.CharField(max_length=6)
    dob = models.DateField()
    dolbd = models.DateField(null=True,blank=True)
    city = models.CharField(max_length=20)
    hidemob = models.CharField(max_length=3)
#    reportedTimes = models.IntegerField(null=True,blank=True)
    
class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(max_length=10,null=True,blank=True)
    value = models.TextField(max_length=300)