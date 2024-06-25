from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
# Create your views here.


class ChronicDiseasesViewSet(viewsets.ModelViewSet):
    queryset = ChronicDiseases.objects.all()
    serializer_class = ChronicDiseasesSerializer

class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer
    