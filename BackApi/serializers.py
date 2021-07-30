import django_filters
from rest_framework import serializers

from BackApi.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # fields = '__all__'
        # exclude = ['id', 'join_time', 'update_time']
        exclude = ['join_time', 'update_time']


class EmployeeFilterSet(django_filters.FilterSet):
    join_time = django_filters.DateTimeFromToRangeFilter(field_name='join_time')
    update_time = django_filters.DateTimeFromToRangeFilter(field_name='update_time')
    p_name = django_filters.CharFilter(field_name='p_name')
    # e_name = django_filters.CharFilter(field_name='e_name')

    class Meta:
        model = Employee
        fields = '__all__'
        # fields = ['join_time', 'update_time', 'p_name']
