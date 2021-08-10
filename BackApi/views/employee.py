import datetime

from rest_framework import viewsets
from rest_framework.response import Response

from BackApi.filters.employee import (
    EmployeeNameFilter,
    EmployeeStartTimeFilter,
    EmployeeEndTimeFilter
)
from BackApi.models import Employee
from BackApi.serializers import EmployeeSerializer

filters = [
    EmployeeNameFilter,
    EmployeeStartTimeFilter,
    EmployeeEndTimeFilter,
]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.filter(isDelete=False).order_by('eName', 'eAge')
    serializer_class = EmployeeSerializer
    filter_backends = filters

    def create(self, request, *args, **kwargs):
        data = request.data
        res = EmployeeSerializer(data=data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 201, 'message': '新增成功'})
        else:
            return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def delete(self, request, *args, **kwargs):
        eId = request.POST.get('id')
        """ 删除之前的逻辑判断 """
        if not eId or not Employee.objects.filter(id=eId) or \
                Employee.objects.filter(id=eId).values("isDelete")[0]['isDelete']:
            return Response({'code': 400, 'message': '删除的id不存在或者传参错误'})

        data = request.data.copy()
        data['isDelete'] = True
        data['updateTime'] = datetime.datetime.now()
        origin_data = Employee.objects.filter(id=eId).first()
        res = EmployeeSerializer(data=data, instance=origin_data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 200, 'message': '删除成功'})
        return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def put(self, request, *args, **kwargs):
        """ 只能更新 e_job,province,city """
        check_fields = ['id', 'eJob', 'province', 'city']
        update_data = request.data.copy()
        eId = update_data['id']

        """ 更新之前的逻辑判断,只能更新未删除状态的数据 """
        if not eId or self.filter_queryset(self.queryset).filter(id=eId) or set(update_data) > set(check_fields):
            return Response({'code': 400, 'message': '更新的id不存在或者传参错误'})

        update_data['updateTime'] = datetime.datetime.now()
        origin_data = Employee.objects.filter(id=eId).first()
        res = EmployeeSerializer(data=update_data, instance=origin_data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 200, 'message': '更新成功'})
        return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})
