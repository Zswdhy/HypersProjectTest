from django.urls import path, include
from rest_framework import routers

from .views.employee import EmployeeViewSet

# from .views.projectsDetails import ProjectsDetailsViewSet
# from .views.projectsList import ProjectsListViewSet

router = routers.DefaultRouter()
router.register('employee', EmployeeViewSet)
# router.register('projectList', ProjectsListViewSet)
# router.register('projectsDetail', ProjectsDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
