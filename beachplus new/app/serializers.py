from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.encoding import force_str



class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, detail2,field2,status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail),field2: int(force_str(detail2))}
        else: self.detail = {'detail': force_str(self.default_detail)}


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email','password')
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True}
        # }

    def create(self, validated_data):

        user = User.objects.create_user(
            
            email=validated_data['email'],
            username=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],     
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# class SignupSerializer(serializers.ModelSerializer):
    
#     def validate(self, value):
#         if User.objects.filter(email=value['email']):
#             raise CustomValidation('Email already exists.','msg',400,'status', status_code=status.HTTP_200_OK)
#         return value

#     class Meta:
#         model = User
#         fields = ('id', 'email', 'password')
#         extra_kwargs = {'password':{'write_only':True}}
        
#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['email'], validated_data['email'], validated_data['password'])
#         return user        


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','first_name','last_name']


class DeviceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Device
        fields="__all__"

    def create(self,validated_data):
        D=Device.objects.create(**validated_data)
        return D


    
class DeviceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Device
        fields="__all__"

    def create(self,validated_data):
        D=Device.objects.create(**validated_data)
        return D


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=("__all__")

    def create(self,validated_data):
        P=Profile.objects.create(**validated_data)
        return P



class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactUs
        fields="__all__"
        def create(self,validated_data):
            C=ContactUs.objects.create(**validated_data)
            return C


class HostMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model=HostMatch
        fields="__all__"

        def create(self,validated_data):
            H=HostMatch.objects.create(**validated_data)
            return H



class ProfileSerializer1(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=("__all__")  

class HostMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model=HostMatch
        fields="__all__"             



class HostInvitationSerializer(serializers.ModelSerializer):
    # hostmatch_id=HostMatchSerializer(read_only=True)
    # user_invited=ProfileSerializer1(read_only=True)
    class Meta:
        model=HostInvitation
        fields="__all__"



class GetHostMatchSerializer(serializers.ModelSerializer):
    # hostmatch=HostInvitationSerializer(many=True)
    class Meta:
        model=HostMatch
        fields="__all__"



class GetProfileSerializer1(serializers.ModelSerializer):
    profile=HostInvitationSerializer(many=True)
    class Meta:
        model=Profile
        fields=("__all__")
class ProfileSerializer1(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=("__all__")  
