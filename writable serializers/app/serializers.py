from rest_framework import serializers
from setuptools import Require
from .models import *



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ingredients
        fields="__all__"
        

class RecipeSerializer(serializers.ModelSerializer):
    # ingredients=IngredientSerializer(many=True,required=False)

    class Meta:
        model=Recipe
        fields="__all__"

        

    # def create(self,validated_data):
           
    #     recipe = Recipe.objects.create(**validated_data)
    #     # ingredient=Ingredients.objects.create(**validated_data)
    #     return recipe
        

        

            
    
    

# class UserSerializer(serializers.ModelSerializer):
#     profile=ProfileSerializer()
#     class Meta:
#         model=User
#         fields = ['username', 'email','profile']

    # def create(self,validated_data):
    #         profile_data=validated_data.pop('profile')
    #         user = User.objects.create(**validated_data)
    #         Profile.objects.create(user=user, **profile_data)
    #         return user    


        
