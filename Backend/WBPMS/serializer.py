from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User
  
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"
class JemoMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = JemoMedicine
        fields = "__all__"
        
class LebuMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LebuMedicine
        fields = "__all__"

class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class userSerializer(serializers.ModelSerializer):
    tele = serializers.CharField(source='profile.tele')
    branch = serializers.CharField(source='profile.branch')
    class Meta:
        model = User
        fields = "__all__"
        
class ProfileSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Profile
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
            model = User
            fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user
