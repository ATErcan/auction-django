from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):
  
  email = serializers.EmailField(required=True, validators = [UniqueValidator(queryset=User.objects.all())])
  password = serializers.CharField(
    required=True, write_only=True, 
    validators=[validate_password],
    style = {
      'input_type':'password',
    }
  )
  
  password2 = serializers.CharField(
    required=True, 
    write_only=True,
    style = {
      'input_type':'password',
    }
  )
  
  class Meta:
    model = User
    fields = (
      "id",
      'username',
      'first_name',
      'last_name',
      'email',
      'password',
      'password2',
    )
    
  def create(self, validated_data):
    password = validated_data.pop("password")
    validated_data.pop('password2')
    user = User.objects.create(**validated_data)
    user.set_password(password)
    user.save()
    return user
  
  def validate(self, data):
    if data.get('password') != data.get('password2'):
      data = {
        "password": "Password fields do not match!"
      }
      raise serializers.ValidationError(data)
    return data
  
class UserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = (
      'id',
      'username',
      'first_name',
      'last_name',
      'email',
    )
    
class CustomTokenSerializer(TokenSerializer):
  
  user = UserSerializer(read_only=True)
  
  class Meta(TokenSerializer.Meta):
    fields = (
      'key',
      'user'
    )
    

class UserUpdateSerializer(serializers.ModelSerializer):
  
  email = serializers.EmailField(required=False)
  
  class Meta:
    model = User
    fields = (
      'id',
      'username',
      'first_name',
      'last_name',
      'email',
    )
    
  def update(self, instance, validated_data):
    instance = super().update(instance, validated_data)
    instance.email = self.context['request'].user.email
    instance.save()
    return instance