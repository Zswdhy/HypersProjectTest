import arrow
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import BaseFilterBackend

from utils.get_params import get_value_from_request


class EmployeeNameFilter(BaseFilterBackend):
    """行业过滤."""

    param = "name"
    title = _("客户name选择")

    def filter_queryset(self, request, queryset, view):
        """来源过滤."""
        param = get_value_from_request(request, self.param)
        if param:
            queryset = queryset.filter(eName__istartswith=param)
        return queryset


class EmployeeStartTimeFilter(BaseFilterBackend):
    """行业过滤."""

    param = "startTime"
    title = _("开始时间")

    def filter_queryset(self, request, queryset, view):
        """行业过滤."""
        param = get_value_from_request(request, self.param)
        if param and arrow.get(param):
            queryset = queryset.filter(updateTime__gte=param)
        return queryset


class EmployeeEndTimeFilter(BaseFilterBackend):
    """行业过滤."""

    param = "endTime"
    title = _("结束时间")

    def filter_queryset(self, request, queryset, view):
        """行业过滤."""
        param = get_value_from_request(request, self.param)
        if param and arrow.get(param):
            queryset = queryset.filter(updateTime__lte=param)
        return queryset


class EmployeeProjectNameFilter(BaseFilterBackend):
    """行业过滤."""

    param = "pname"
    title = _("项目名称")

    def filter_queryset(self, request, queryset, view):
        """行业过滤."""
        param = get_value_from_request(request, self.param)
        if param and arrow.get(param):
            queryset = queryset.filter(p_name=param)
        return queryset
