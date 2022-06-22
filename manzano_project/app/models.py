from django.db import models
from django.contrib.auth.models import User
import django

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_image',blank=True,null=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    zip=models.CharField(max_length=100,null=True,blank=True)
    cpf_number=models.CharField(max_length=100,null=True,blank=True)
    date_added=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.first_name

class Report(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    image=models.ImageField(upload_to='report_image',blank=True,null=True)
    feedback=models.TextField(max_length=300,null=True,blank=True)


class Buisness(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(upload_to='buisness_image',blank=True,null=True)
    address=models.CharField(max_length=100,blank=True,null=True)

def __str__(self):
    return self.name
