from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

import tensorflow as tf
import numpy as np
import cv2

meat_model = tf.keras.models.load_model('my_meat_model.h5')
print("Model Initialization :)")

# Create your views here.

class ProductStoreViewSet(viewsets.ModelViewSet):
    queryset = ProductStore.objects.all()
    serializer_class = ProductStoreSerializer


class ProductComponentViewSet(viewsets.ModelViewSet):
    queryset = ProductComponent.objects.all()
    serializer_class = ProductComponentSerializer

class DiseaseTypeViewSet(viewsets.ModelViewSet):
    queryset = DiseaseType.objects.all()
    serializer_class = DiseaseTypeSerializer

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class MeatDetectionViewSet(viewsets.ModelViewSet):
    queryset = MeatDetection.objects.all()
    serializer_class = MeatDetectionSerializer

    def perform_create(self, serializer):
        result = serializer.save()

        image_url = serializer.instance.image.path
        # Here is performing the AI model logic :)
        detection_result = self.detection(image_url)

        if detection_result == 1:
            result.result_class = detection_result
            result.result = 'Fresh or half fresh'
        else:
            result.result_class = detection_result
            result.result = 'Spoiled'

        result.save()
        
    def detection(self, image_input):
        img = cv2.imread(image_input)
        img = cv2.resize(img, (256, 256))
        img = np.array(img)
        # img = img / 255.0
        img = np.expand_dims(img, axis=0)
        prediction = meat_model.predict(img)
        class_idx = np.argmax(prediction, axis=1)
        # print("#" * 50)
        # print(prediction)
        # print(class_idx)
        return class_idx[0]