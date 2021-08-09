import django_filters
from rest_framework import serializers

from BackApi.models import Employee, ProjectsList, ProjectsDetails


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


""" 项目列表页 """


class ProjectsListSerializer(serializers.ModelSerializer):
    # p_name = serializers.CharField(label='项目名称')
    # p_start_time = serializers.DateField(label='项目开始时间')
    # p_end_time = serializers.DateField(label='项目结束时间')

    class Meta:
        model = ProjectsList
        # fields = ['p_name', 'p_start_time', 'p_end_time', 'employee_num', 'user_id']
        fields = '__all__'
        # exclude = ['is_delete']


""" 项目详情页 """


class ProjectsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsDetails
        fields = '__all__'
