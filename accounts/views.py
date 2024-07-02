from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
# Create your views here.


class DiabetesNutrientsViewSet(viewsets.ModelViewSet):
    queryset = DiabetesNutrients.objects.all()
    serializer_class = DiabetesNutrientsSerializer

class HypertensionNutrientsViewSet(viewsets.ModelViewSet):
    queryset = HypertensionNutrients.objects.all()
    serializer_class = HypertensionNutrientsSerializer
    
class AllergyNutrientsViewSet(viewsets.ModelViewSet):
    queryset = AllergyNutrients.objects.all()
    serializer_class = AllergyNutrientsSerializer
    