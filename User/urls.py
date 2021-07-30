from django.urls import path, include
from rest_framework import routers

from .views import (
    first_test, UserViewSet
)

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/', first_test),  # test api
]
