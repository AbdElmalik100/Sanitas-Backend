import json
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from accounts.models import *
from django.forms.models import model_to_dict

import tensorflow as tf
import numpy as np
import cv2
import hashlib
from pathlib import Path
import google.generativeai as genai



meat_model = tf.keras.models.load_model('my_meat_model.h5')
class Extract_info:
    def __init__(self, API_KEY: str):
        genai.configure(api_key=API_KEY)

        # Set up the model
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )

        self.uploaded_files = []

    def upload_if_needed(self, pathname: str) -> list[str]:
        path = Path(pathname)
        hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
        try:
            existing_file = genai.get_file(name=hash_id)
            return [existing_file]
        except:
            pass
        self.uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
        return [self.uploaded_files[-1]]

    def extract(self, image_path: str, prompt: str = "Extract info from image"):
        prompt_parts = [
            "\n\n\n",
            *self.upload_if_needed(image_path),
            prompt,
        ]

        response = self.model.generate_content(prompt_parts)
        for uploaded_file in self.uploaded_files:
            genai.delete_file(name=uploaded_file.name)

        return response.text

print("Model Initialization :)")


class ProductStoreViewSet(viewsets.ModelViewSet):
    queryset = ProductStore.objects.all()
    serializer_class = ProductStoreSerializer


class ProductComponentViewSet(viewsets.ModelViewSet):
    queryset = ProductComponent.objects.all()
    serializer_class = ProductComponentSerializer

    def perform_create(self, serializer):
        result = serializer.save()

        image_url = serializer.instance.image.path

        nutrition_list = self.detection(image_url)
        
        result.nutritions = nutrition_list
        detection_result = self.check_limits(nutrition_list)

        if detection_result: 
            result.result = "rejected"
            result.result_class = 1
        else:
            result.result = "approval"
            result.result_class = 0
        result.save()

    def detection(self, imageUrl):
        extract_obj = Extract_info(API_KEY = "AIzaSyASK5dADQhFR8H1PPBm4-Ddq9esF_SFM8E")
        text = extract_obj.extract(
                        image_path = imageUrl,
                        prompt = "Extract Saturated fat, Trans fat, Cholesterol, Sodium, Dietary fiber, Total sugars, Added sugars, Gluten, Lactose, Egg from this image in points, don't use markdown text"
                    )
        return self.json_converter(text)

    def check_limits(self, detectionResult):
        checker = []

        diabetes = ['total_sugars', 'added_sugars']
        hypertension = ['sodium', 'saturated_fat', 'trans_fat', 'cholesterol']
        allergy = ['gluten', 'lactose', 'egg']

        acceptable_limits = { # Deal with this - g, ml
            'saturated_fat': 15.56,     # حدود الشحوم المشبعة: 15.56 جم
            'trans_fat': 0,             # لا يجب أن يكون هناك دهون متحولة
            'cholesterol': 200,         # 200 ملغ هو الحد الأقصى للكوليسترول
            'sodium': 2300,             # 2300 ملغ هو الحد الأقصى للصوديوم
            'dietary_fiber': 30,        # 30 غرام هو الحد الأدنى للألياف الغذائية
            'total_sugars': 50,         # 50 غرام هو الحد الأقصى للسكريات الإجمالية
            'added_sugars': 0           # يجب ألا تحتوي السكريات المضافة على قيمة
        }

        diabetes_nutrients = DiabetesNutrients.objects.filter(user = self.request.user)
        hypertension_nutrients = HypertensionNutrients.objects.filter(user = self.request.user)
        allergy_nutrients = AllergyNutrients.objects.filter(user = self.request.user)

        for nutrient in diabetes_nutrients:
            nutrient_dict = model_to_dict(nutrient)
            for key, value in nutrient_dict.items():
                if key == 'diabetes':
                    if value:
                        for item in diabetes:
                            if item in detectionResult and 'Not' not in detectionResult[item]:
                                if self.convert_to_float(detectionResult[item]) > acceptable_limits[item]:
                                    checker.append('rejected')
                                else: checker.append('approval')
                    else:
                        checker.append('approval')

        for nutrient in hypertension_nutrients:
            nutrient_dict = model_to_dict(nutrient)
            for key, value in nutrient_dict.items():
                if key == 'hypertension':
                    if value:
                        for item in hypertension:
                            if item in detectionResult and 'Not' not in detectionResult[item]:
                                if self.convert_to_float(detectionResult[item]) > acceptable_limits[item]:
                                    checker.append('rejected')
                                else: checker.append('approval')
                    else:
                        checker.append('approval')
        
        for nutrient in allergy_nutrients:
            nutrient_dict = model_to_dict(nutrient)
            for key, value in nutrient_dict.items():
                if key in allergy:
                    if value:
                        for item in allergy:
                            if item in detectionResult and 'Not' not in detectionResult[item]:
                                print(item)
                                print(detectionResult[item])
                                if self.convert_to_float(detectionResult[item]) > acceptable_limits[item]:
                                    checker.append('rejected')
                                else: checker.append('approval')
                    else:
                        checker.append('approval')

        print(checker)
        return True if 'rejected' in checker else False



                    # if value and (diabetes[0] in detectionResult or diabetes[1] in detectionResult) and (self.convert_to_float(detectionResult[diabetes[0]]) > acceptable_limits[diabetes[0]] or self.convert_to_float(detectionResult[diabetes[1]]) > acceptable_limits[diabetes[1]]):
                    #     true_counter += 1
                    # else:
                    #     false_counter += 1

                # if key in detectionResult and detectionResult[key] != 'Not specified':
                #     acceptable_limits[key] = value
                    

        # for nutrient in hypertension_nutrients:
        #     nutrient_dict = model_to_dict(nutrient)
        #     for key, value in nutrient_dict.items():
        #         if key in detectionResult and detectionResult[key] != 'Not specified':
        #             if value:
        #                 true_counter += 1
        #             else:
        #                 false_counter += 1
        #             acceptable_limits[key] = value

        # for nutrient in allergy_nutrients:
        #     nutrient_dict = model_to_dict(nutrient)
        #     for key, value in nutrient_dict.items():
        #         if key in detectionResult and detectionResult[key] != 'Not specified':
        #             if value:
        #                 true_counter += 1
        #             else:
        #                 false_counter += 1
        #             acceptable_limits[key] = value
        # print(acceptable_limits)
        # print("true count", true_counter)
        # print("false count", false_counter)
        # print("length", int(len(acceptable_limits)))
        # if true_counter > int(len(acceptable_limits)) - 2:
        #     return "rejected"
        # elif false_counter > int(len(acceptable_limits)) -2:
        #     return "approval"
        # else:
        #     return "normalize"

    # def check_limits(self, detectionResult):
    #     acceptable_limits = { # DEal with this - g, ml
    #         'Saturated Fat': 15.56,     # حدود الشحوم المشبعة: 15.56 جم
    #         'Trans Fat': 0,             # لا يجب أن يكون هناك دهون متحولة
    #         'Sodium': 2300,             # 2300 ملغ هو الحد الأقصى للصوديوم
    #         'Dietary Fiber': 30,        # 30 غرام هو الحد الأدنى للألياف الغذائية

    #         #Chronic Disease
    #         'Cholesterol': 200,         # 200 ملغ هو الحد الأقصى للكوليسترول
    #         'Total Sugars': 50,         # 50 غرام هو الحد الأقصى للسكريات الإجمالية
    #         'Added Sugars': 0           # يجب ألا تحتوي السكريات المضافة على قيمة
    #     }
    #     for nutrient, value in detectionResult.items():
    #         if nutrient in acceptable_limits:
    #             max_limit = acceptable_limits[nutrient]
    #             if value.endswith("mg"):
    #                 value = value.replace("mg", "")
    #             elif value.endswith("%"):
    #                 value = value.replace("%", "")
    #             else:
    #                 value = value.replace("g", "")
    #             # value = value.replace("mg", "") if value.endswith("mg") else value.replace("g", "")
    #             return False if float(value) > max_limit else True

    def json_converter(self, text):
        nutrients = {}
        lines = text.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("*") or line.startswith("-"):
                # Split based on ":" to handle both formats
                key_value = line.replace("*", "").replace("-", "").strip().split(": ")
                if len(key_value) == 2:
                    nutrient = "_".join(key_value[0].strip().lower().split(" "))
                    value = key_value[1].strip()
                    nutrients[nutrient] = value
        return nutrients
    
    def convert_to_float(self, s):
        number = ''.join(filter(lambda x: x.isdigit() or x == '.', s))
        return float(number)
    
    

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
        
        return class_idx[0]