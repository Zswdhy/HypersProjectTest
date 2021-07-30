from django.urls import path, include
from rest_framework import routers

from BackApi.views import back_api_test, EmployeeViewSet

router = routers.DefaultRouter()
router.register('employee', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/', back_api_test),
]
