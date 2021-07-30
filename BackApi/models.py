from django.db import models

""" 项目列表 model  """

# class ProjectsList(models.Model):
#     id = models.IntegerField(primary_key=True)
#     p_name = models.CharField(max_length=64)
#     p_start_time = models.DateTimeField(auto_now=True, null=True, blank=True)
#     p_end_time = models.DateTimeField(auto_now=True, null=True, blank=True)
#     employee_num = models.IntegerField(default=0)
#     user_id = models.IntegerField()
#     is_delete = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'project_list'
#
#
# """ 项目详情 model """
#
#
# class ProjectsDetails(models.Model):
#     pd_id = models.IntegerField(primary_key=True)
#     id = models.ForeignKey('ProjectsList', on_delete=models.CASCADE)
#     p_name = models.CharField(max_length=64)
#     p_introduce = models.CharField(max_length=255)
#     e_name = models.CharField(max_length=32)
#     e_age = models.IntegerField()
#
#     class Meta:
#         db_table = 'project_details'


""" 客户 model """


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=64)
    e_age = models.IntegerField()
    e_job = models.CharField(max_length=64, null=True, blank=True)
    province = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    p_name = models.CharField(max_length=64)
    join_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'employee'
