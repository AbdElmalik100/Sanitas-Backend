from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


class ChronicDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicDiseases
        fields = '__all__'
    
class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'



class CustomUserSerializer(UserSerializer):
    user_chronic_disease = ChronicDiseasesSerializer(many = True, read_only = True)
    user_allergy = AllergySerializer(many = True, read_only = True)
    
    class Meta:
        model = get_user_model()
        exclude = ['groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser', 'password']


