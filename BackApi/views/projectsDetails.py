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
        check_fields = ['pId', 'pIntroduce', 'eId']
        data = request.data.copy()

        """ 传参的校验 """
        if set(data) != set(check_fields) or \
                not ProjectsList.objects.filter(id=data['pId']) or \
                not Employee.objects.filter(id=data['eId']):
            return Response({'code': 400, 'message': '更新的id不存在或者传参错误'})
        """一个客户只能属于一个项目."""
        if ProjectsDetails.objects.filter(eId=data['eId']):
            return Response({'code': 400, 'message': '一个客户只属于一个项目'})

        """ 获取项目名称和现有项目人数，以及项目人数的判定 """
        p_details = ProjectsList.objects.filter(id=data['pId']).values('pName', 'employee_num')[0]
        if p_details['employee_num'] >= PROJECT_EMPLOYEE:
            return Response({'code': 400, 'message': '本项目的客户已达到上限'})
        data.update(p_details)

        e_details = Employee.objects.filter(id=data['eId']).values('eName', 'eAge')[0]
        data.update(e_details)
        data['id'] = int(data['pId'])

        """ 保存 """
        res = ProjectsDetailsSerializer(data=data, partial=True)
        if res.is_valid():
            res.save()

            """更新项目列表客户字段"""
            p_date = {'employee_num': int(p_details['employee_num']) + 1}
            ProjectsList.objects.filter(id=data['pId']).update(**p_date)

            """更新客户的部分字段"""
            e_data = {'id': data['eId'], 'isInProject': True, 'pName': p_details['pName'],
                      'updateTime': datetime.datetime.now()}
            Employee.objects.filter(id=data['eId']).update(**e_data)

            return Response({'code': 201, 'message': '新增成功'})
        else:
            return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def delete(self, request, *args, **kwargs):
        """删除单独的客户."""
        pk = request.POST.get('eId')
        """用户权限."""
        if ProjectsList.objects.filter(
                id=ProjectsDetails.objects.filter(eId=pk).values('pId')[0]['pId']) \
                .values('userId')[0]['userId'] != request.user.id:
            return Response({'code': 400, 'message': '无修改权限'})

        if not pk or not ProjectsDetails.objects.filter(eId=int(pk)):
            return Response({'code': 400, 'message': '删除的客户id不存在'})

        ProjectsDetails.objects.filter(eId=int(pk)).delete()
        origin_data = Employee.objects.filter(id=pk).first()
        data = {'isInProject': False, 'pName': None, 'updateTime': datetime.datetime.now()}
        res = EmployeeSerializer(data=data, instance=origin_data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 200, 'message': '删除成功'})

        return Response({'code': 400, 'message': '删除失败', 'error': res.errors})
