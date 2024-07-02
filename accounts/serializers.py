from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


class DiabetesNutrientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiabetesNutrients
        fields = '__all__'
    
class HypertensionNutrientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HypertensionNutrients
        fields = '__all__'
class AllergyNutrientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllergyNutrients
        fields = '__all__'



class CustomUserSerializer(UserSerializer):
    user_diabetes_nutrients = DiabetesNutrientsSerializer(many = True, read_only = True)
    user_hypertension_nutrients = HypertensionNutrientsSerializer(many = True, read_only = True)
    user_allergy_nutrients = AllergyNutrientsSerializer(many = True, read_only = True)
    
    class Meta:
        model = get_user_model()
        exclude = ['groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser', 'password']


