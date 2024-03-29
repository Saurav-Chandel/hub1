from django.db import models

# Create your models here.

class Country(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    population=models.IntegerField()
    country=models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return self.name