from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.

def back_api_test(request):
    return JsonResponse({'code': 200, 'message': 'test 通过'})
