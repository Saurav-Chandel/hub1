from django.db import models
from django.contrib.auth.models import User

# Create your mode

class Ingredients(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    description=models.CharField(max_length=100,null=True,blank=True)
    ingredients=models.ManyToManyField(Ingredients)

    def __str__(self):
        return self.name








# class Profile(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     profile_image=models.ImageField(upload_to='profile',blank=True,null=True)
#     city=models.CharField(max_length=100,null=True,blank=True)
#     state=models.CharField(max_length=100,null=True,blank=True)
