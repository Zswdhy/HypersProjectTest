from django.http import JsonResponse
from rest_framework import viewsets

from rest_framework_simplejwt.views import TokenObtainPairView

from User.models import User
from User.serializers import UserModelSerializer, MyTokenObtainPairSerializer


def first_test(request):
    return JsonResponse({'code': 200, 'message': 'test success'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
