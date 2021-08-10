from rest_framework import serializers

from BackApi.models import Employee, ProjectsList, ProjectsDetails


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


""" 项目列表页 """


class ProjectsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsList
        fields = '__all__'


""" 项目详情页 """


class ProjectsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsDetails
        fields = '__all__'
