from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()

router.register('chronic_disease', ChronicDiseasesViewSet)
router.register('allergy', AllergyViewSet)


urlpatterns = [
    path('', include(router.urls))
]
