from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response

from BackApi.models import ProjectsList
from BackApi.serializers import ProjectsListSerializer


class ProjectsListViewSet(viewsets.ModelViewSet):
    queryset = ProjectsList.objects.all()
    serializer_class = ProjectsListSerializer

    # authentication_classes = []
    # permission_classes = []

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

    def list(self, request, *args, **kwargs):
        """
            未完成：admin和member用户的区别显示
        """
        p_name = request.GET.get('p_name')
        category = request.user.category
        print('category', category)
        if p_name:
            data = ProjectsList.objects.filter(p_name__istartswith=p_name)
            res = [model_to_dict(item) for item in data]
            return Response({'code': 200, 'data': res})
        else:
            data = ProjectsList.objects.all()
            res = [model_to_dict(item) for item in data]
            return Response({'code': 200, 'data': res})
