from rest_framework import serializers
from api.models import *
from django.contrib.auth.hashers import make_password
from api.tokens import generate_access_token, generate_refresh_token


## User SignUp Serializer.
class UserSignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(min_length=6,max_length=100, write_only=True)
   
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password',)

    def validate(self, attrs):
        email = attrs.get('email')
        email_check = User.objects.filter(email=email).exists()
        if email_check:
            raise serializers.ValidationError({'error' : 'Email already exists.'})
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['username'] = validated_data.get('email')
        validated_data['roles_id'] = 2 ## Employee type role id is 2
        return super(UserSignUpSerializer, self).create(validated_data)


### User Login Serializer.
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100,error_messages={'blank': 'Please enter email address'})
    password = serializers.CharField(min_length=6,max_length=128,error_messages={'blank': 'Please enter password'},write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('name','email','password','access_token','refresh_token',)
        

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.filter(email=email).last()
        if user is None:
            raise serializers.ValidationError({'error' : 'User not found.'})
        if (not user.check_password(password)):
            raise serializers.ValidationError({'error' : 'Email or Password incorrect.Please try again.'})
        ## Access Token.
        if user.is_active == False:
            raise serializers.ValidationError({'error' : 'Account is inactive.Please contact your administrator'})
        attrs['access_token'] = generate_access_token(user.id)
        ## Refresh Token.
        attrs['refresh_token'] = generate_refresh_token(user.id)
        attrs['name'] = f"{user.first_name} {user.last_name}"
        return super().validate(attrs)

### User Forecast Store Searializer.

class UserForecastStoreSearializer(serializers.ModelSerializer):
    class Meta:
        model = UserForecastStore
        fields = '__all__'