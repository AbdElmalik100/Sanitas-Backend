from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()

router.register('diabetes-nutrients', DiabetesNutrientsViewSet)
router.register('hypertension-nutrients', HypertensionNutrientsViewSet)
router.register('allergy-nutrients', AllergyNutrientsViewSet)


urlpatterns = [
    path('', include(router.urls))
]
