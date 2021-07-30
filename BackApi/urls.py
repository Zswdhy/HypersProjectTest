from django.urls import path

from BackApi.views import back_api_test

urlpatterns = [
    path('test/', back_api_test),
]
