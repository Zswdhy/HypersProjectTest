import datetime

from paraer.vendor import HTTPPaginator
from rest_framework import viewsets
from rest_framework.response import Response

from BackApi.models import ProjectsList, ProjectsDetails, Employee
from BackApi.serializers import ProjectsListSerializer


class ProjectsListViewSet(viewsets.ModelViewSet):
    queryset = ProjectsList.objects.all()
    serializer_class = ProjectsListSerializer
    pagination_class = HTTPPaginator

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['employee_num'] = 0
        data['userId'] = request.user.id
        data['isDelete'] = False
        res = ProjectsListSerializer(data=data, partial=True)
        if res.is_valid():
            res.save()
            return Response({'code': 201, 'message': '新增成功'})
        else:
            return Response({'code': 400, 'message': '数据校验失败', 'error': res.errors})

    def delete(self, request, *args, **kwargs):
        p_id = request.POST.get('pId')
        if not p_id or not self.filter_queryset(self.queryset).filter(id=int(p_id)):
            return Response({'code': 400, 'message': '传参错误'})

        update_data = {'employee_num': 0, 'isDelete': True}
        origin_data = ProjectsList.objects.filter(id=p_id).first()
        res = ProjectsListSerializer(data=update_data, instance=origin_data, partial=True)
        if res.is_valid():
            res.save()
            # 删除项目详情页数据
            ProjectsDetails.objects.filter(pId=p_id).delete()
            # 更新客户的项目状态
            e_id = ProjectsDetails.objects.filter(pId=p_id).values_list('eId')
            date = {'isInProject': False, 'pName': None, 'updateTime': datetime.datetime.now()}
            Employee.objects.filter(id__in=e_id).update(**date)
            return Response({'code': 200, 'message': '删除成功'})
        return Response({'code': 400, 'message': '校验失败', 'error': res.errors})

    def list(self, request, *args, **kwargs):

        catalogue = request.user.category

        if catalogue != 'admin':
            queryset = self.filter_queryset(self.queryset).filter(userId=request.user.id)
        else:
            queryset = self.filter_queryset(self.queryset)
        serializer = self.get_serializer(queryset, many=True)
        dataset = self.paginate_queryset(serializer.data)
        return Response(dataset)
