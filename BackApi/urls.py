from django.urls import path, include
from rest_framework import routers

from .views.employee import EmployeeViewSet
from .views.projects import ProjectsListViewSet

router = routers.DefaultRouter()
router.register('employee', EmployeeViewSet)
router.register('projectList', ProjectsListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
