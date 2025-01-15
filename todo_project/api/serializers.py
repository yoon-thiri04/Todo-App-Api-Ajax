from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model= Task
        fields= "__all__"

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields= ['username', 'email', 'password', 'confirm_password']
        extra_kwargs= {
            'password': {'write_only':True},
        }

    def validate(self, data):

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'password':"Passwords must match."})

        return data

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('An account with this email already exits.')
        return value

    def create(self, validated_data):

        validated_data.pop('confirm_password') #Remove confirm_password from validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password= serializers.CharField(write_only=True)

    def validate(self,data):
        username=data.get('username')
        password=data.get('password')

        user=authenticate(username=username,password=password)

        if user is None:
            raise serializers.ValidationError({'Invalid':'Invalid Username or Password.'})
        return {'user':user}

