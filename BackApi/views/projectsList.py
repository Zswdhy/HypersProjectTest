import datetime

from django.db.models import Q
from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response

from BackApi.models import ProjectsList, ProjectsDetails, Employee
from BackApi.serializers import ProjectsListSerializer


class ProjectsListViewSet(viewsets.ModelViewSet):
    queryset = ProjectsList.objects.filter(is_delete=False)
    serializer_class = ProjectsListSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['employee_num'] = 0
        data['user_id'] = request.user.id
        data['is_delete'] = False
        res = ProjectsListSerializer(data=data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 201, 'message': '新增成功'})
        else:
            return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def delete(self, request, *args, **kwargs):
        p_id = request.POST.get('id')
        if not p_id or not self.queryset.filter(id=int(p_id)):
            return Response({'code': 400, 'message': '传参错误'})

        update_data = {'employee': 0, 'is_delete': True}
        origin_data = ProjectsList.objects.filter(id=p_id).first()
        res = ProjectsListSerializer(data=update_data, instance=origin_data, partial=True)
        if res.is_valid():
            # res.save()
            e_id = ProjectsDetails.objects.filter(p_id=p_id).values_list('e_id')
            print('e_id', e_id, type(e_id))
            date = {'is_in_project': False, 'p_name': None, 'update_time': datetime.datetime.now()}
            Employee.objects.filter(id__in=e_id).update(**date)
            return Response({'code': 200, 'message': '删除成功'})
        return Response({'code': 400, 'message': '校验失败', 'error': res.errors})

    def list(self, request, *args, **kwargs):
        p_name = request.GET.get('p_name')
        catalogue = request.user.category
        if p_name:
            if catalogue != 'admin':
                data = self.queryset.filter(Q(p_name__istartswith=p_name) & Q(user_id=int(request.user.id)))
                res = [model_to_dict(item) for item in data]
                return Response({'code': 200, 'data': res})
            else:
                data = self.queryset.filter(Q(p_name__istartswith=p_name))
                res = [model_to_dict(item) for item in data]
                return Response({'code': 200, 'data': res})

        if catalogue != 'admin':
            data = self.queryset.filter(Q(user_id=int(request.user.id)))
            res = [model_to_dict(item) for item in data]
            return Response({'code': 200, 'data': res})
        else:
            data = self.queryset.filter()
            res = [model_to_dict(item) for item in data]
            return Response({'code': 200, 'data': res})
