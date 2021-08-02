import datetime
import time

from django.db.models import Q
from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.response import Response

from BackApi.models import Employee
from BackApi.serializers import EmployeeSerializer, EmployeeFilterSet


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer
    filter_class = EmployeeFilterSet
    # filter_fields = ('e_age', 'e_name')
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    def create(self, request, *args, **kwargs):
        data = request.data
        res = EmployeeSerializer(data=data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 201, 'message': '新增成功'})
        else:
            return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def delete(self, request, *args, **kwargs):
        e_id = request.POST.get('id')
        """ 删除之前的逻辑判断 """
        if not e_id or not Employee.objects.filter(id=e_id) or \
                Employee.objects.filter(id=e_id).values("is_delete")[0]['is_delete']:
            return Response({'code': 400, 'message': '删除的id不存在或者传参错误'})

        data = request.data.copy()
        data['is_delete'] = True
        data['update_time'] = datetime.datetime.now()
        origin_data = Employee.objects.filter(id=e_id).first()
        res = EmployeeSerializer(data=data, instance=origin_data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 200, 'message': '删除成功'})
        return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def put(self, request, *args, **kwargs):
        """ 只能更新 e_job,province,city """
        check_fields = ['id', 'e_job', 'province', 'city']
        update_data = request.data.copy()
        e_id = update_data['id']

        """ 更新之前的逻辑判断 """
        if not e_id or not Employee.objects.filter(id=e_id) or set(update_data) > set(check_fields):
            return Response({'code': 400, 'message': '更新的id不存在或者传参错误'})

        update_data['update_time'] = datetime.datetime.now()
        origin_data = Employee.objects.filter(id=e_id).first()
        res = EmployeeSerializer(data=update_data, instance=origin_data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 200, 'message': '删除成功'})
        return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def list(self, request, *args, **kwargs):
        join_time_start = request.GET.get('join_time_start')
        join_time_end = request.GET.get('join_time_end')
        e_name = request.GET.get('e_name')
        if join_time_start and join_time_end:
            start = time.strptime(join_time_start.split('.')[0], '%Y-%m-%d %H:%M:%S')
            end = time.strptime(join_time_end.split('.')[0], '%Y-%m-%d %H:%M:%S')
            start_time = datetime.datetime(start.tm_year, start.tm_mon, start.tm_mday, start.tm_hour, start.tm_min,
                                           start.tm_sec)
            end_time = datetime.datetime(end.tm_year, end.tm_mon, end.tm_mday, end.tm_hour, end.tm_min, end.tm_sec)

            data = Employee.objects.filter(Q(is_delete=False) and Q(join_time__range=(start_time, end_time)))
            res = []
            for item in data:
                temp = model_to_dict(item)
                temp['join_time'] = item.join_time
                res.append(temp)
            return Response({'code': 200, 'data': res})
        elif e_name:
            """ 名称的模糊查询,以 e_name 开头，没使用 contains """
            select_data = Employee.objects.filter(Q(is_delete=False) and Q(e_name__istartswith=e_name))
            res = [model_to_dict(item) for item in select_data]
            return Response({'code': 200, 'data': res})
        else:
            return Response({'code': 400, 'message': '传参数错'})
