"""HypersProjectTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from User.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('User.urls')),  # user api
    path('backapi/', include('BackApi.urls')),  # backend api
]

# simple jwt
urlpatterns += [
    # path('api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 默认返回 token
    path('api-token-auth/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 生成 token
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新 token
]
