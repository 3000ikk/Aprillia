from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, create_payment_intent

router = DefaultRouter()
router.register('', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('create/payment/<int:order_id>/', create_payment_intent, name='create-payment-intent')
]