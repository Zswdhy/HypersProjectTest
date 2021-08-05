from rest_framework import viewsets
from rest_framework.response import Response

from BackApi.models import ProjectsDetails, ProjectsList
from BackApi.serializers import ProjectsDetailsSerializer
from HypersProjectTest.settings import PROJECT_EMPLOYEE


class ProjectsDetailsViewSet(viewsets.ModelViewSet):
    queryset = ProjectsDetails.objects.all()
    serializer_class = ProjectsDetailsSerializer

    def create(self, request, *args, **kwargs):
        check_fields = ['p_id', 'p_introduce', 'e_id']
        data = request.data.copy()

        """ 传参的校验 """
        if set(data) != set(check_fields) or not ProjectsList.objects.filter(id=data['p_id']):
            return Response({'code': 400, 'message': '更新的id不存在或者传参错误'})

        """ 获取项目名称和现有项目人数，以及项目人数的判定 """
        p_details = ProjectsList.objects.filter(id=data['p_id']).values('p_name', 'employee_num')[0]
        if p_details['employee_num'] > PROJECT_EMPLOYEE:
            return Response({'code': 400, 'message': '本项目的客户已达到上限'})
        p_details['employee_num'] += 1
        data.update(p_details)

        """
            一人只能属于一个项目，对应的参数校验
        """

        """ 保存 """
        res = ProjectsDetailsSerializer(data=data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 201, 'message': '新增成功'})
        else:
            return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})
