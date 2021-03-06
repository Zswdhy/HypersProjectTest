import datetime

from rest_framework import viewsets, status
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
    queryset = Employee.objects.filter(isDelete=False)
    serializer_class = EmployeeSerializer
    filter_backends = filters

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        eId = request.POST.get('id')
        """ 删除之前的逻辑判断 """
        if not eId or not self.filter_queryset(self.get_queryset()).filter(id=eId):
            return Response({'message': '删除的id不存在或者传参错误'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['isDelete'] = True
        data['updateTime'] = datetime.datetime.now()
        origin_data = Employee.objects.filter(id=eId).first()
        serializer = EmployeeSerializer(data=data, instance=origin_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'id': eId, 'message': '删除成功'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': '数据校验失败', 'error': serializer.errors})

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
