from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
# from rest_framework.routers import DefaultRouter
# from .views import * 

# router = DefaultRouter()
# router.register('product-store', ProductStoreViewSet)

router = DefaultRouter()
router.register('product-store', ProductStoreViewSet)
router.register('product-component', ProductComponentViewSet)
router.register('disease-type', DiseaseTypeViewSet)
router.register('orders', OrdersViewSet)
router.register('meat-detection', MeatDetectionViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
