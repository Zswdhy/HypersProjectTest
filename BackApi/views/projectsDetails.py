import datetime

from rest_framework import viewsets
from rest_framework.response import Response

from BackApi.models import ProjectsDetails, ProjectsList, Employee
from BackApi.serializers import ProjectsDetailsSerializer, EmployeeSerializer
from HypersProjectTest.settings import PROJECT_EMPLOYEE


class ProjectsDetailsViewSet(viewsets.ModelViewSet):
    queryset = ProjectsDetails.objects.all()
    serializer_class = ProjectsDetailsSerializer

    def create(self, request, *args, **kwargs):
        check_fields = ['p_id', 'p_introduce', 'e_id']
        data = request.data.copy()

        """ 传参的校验 """
        if set(data) != set(check_fields) or \
                not ProjectsList.objects.filter(id=data['p_id']) or \
                not Employee.objects.filter(id=data['e_id']):
            return Response({'code': 400, 'message': '更新的id不存在或者传参错误'})
        """一个客户只能属于一个项目."""
        if ProjectsDetails.objects.filter(e_id=data['e_id']):
            return Response({'code': 400, 'message': '一个客户只属于一个项目'})

        """ 获取项目名称和现有项目人数，以及项目人数的判定 """
        p_details = ProjectsList.objects.filter(id=data['p_id']).values('p_name', 'employee_num')[0]
        if p_details['employee_num'] > PROJECT_EMPLOYEE:
            return Response({'code': 400, 'message': '本项目的客户已达到上限'})
        p_details['employee_num'] += 1
        data.update(p_details)
        e_details = Employee.objects.filter(id=data['e_id']).values('e_name', 'e_age')[0]
        data.update(e_details)
        data['id'] = int(data['p_id'])

        """ 保存 """
        res = ProjectsDetailsSerializer(data=data, partial=True)
        if res.is_valid():
            res.save()

            """更新客户的部分字段"""
            origin_data = Employee.objects.filter(id=data['e_id']).first()
            data = {'id': data['e_id'], 'is_in_project': True, 'p_name': p_details['p_name'],
                    'update_time': datetime.datetime.now()}
            res_2 = EmployeeSerializer(data=data, instance=origin_data, partial=True)
            if res_2.is_valid():
                res_2.save()
            else:
                return Response({'code': 111, 'error': res_2.errors})
            return Response({'code': 201, 'message': '新增成功'})
        else:
            return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def delete(self, request, *args, **kwargs):
        """删除单独的客户."""
        pk = request.POST.get('e_id')
        if not pk or not ProjectsDetails.objects.filter(e_id=int(pk)):
            return Response({'code': 400, 'message': '删除的客户id不存在'})

        ProjectsDetails.objects.filter(e_id=int(pk)).delete()
        origin_data = Employee.objects.filter(id=pk).first()
        data = {'is_in_project': False, 'p_name': None, 'update_time': datetime.datetime.now()}
        res = EmployeeSerializer(data=data, instance=origin_data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 200, 'message': '删除成功'})

        return Response({'code': 400, 'message': '删除失败', 'error': res.errors})
