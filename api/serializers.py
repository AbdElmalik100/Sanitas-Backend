from rest_framework import serializers
from .models import *


class ProductStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStore
        fields = '__all__'

class ProductComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComponent
        fields = '__all__'

class DiseaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseType
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class MeatDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeatDetection
        fields = '__all__'