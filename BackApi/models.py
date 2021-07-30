from django.db import models

""" 项目列表 model  """


class ProjectsList(models.Model):
    id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=64, db_column='项目名称')
    p_start_time = models.DateTimeField(db_column='项目开始时间')
    p_end_time = models.DateTimeField(db_column='项目结束时间')
    employee_num = models.IntegerField(default=0, db_column='项目人数')
    user_id = models.IntegerField(db_column='所属管理员')
    is_delete = models.BooleanField(default=False, db_column='是否删除')

    class Meta:
        db_table = 'project_list'


""" 项目详情 model """


class ProjectsDetails(models.Model):
    pd_id = models.AutoField(primary_key=True)
    id = models.ForeignKey('ProjectsList', on_delete=models.CASCADE, db_column='项目详情 ID')
    p_name = models.CharField(max_length=64, db_column='项目名称')
    p_introduce = models.CharField(max_length=255, db_column='项目介绍')
    e_name = models.CharField(max_length=32, db_column='客户姓名')
    e_age = models.IntegerField(db_column='客户年龄')

    class Meta:
        db_table = 'project_details'


""" 客户 model """


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=64, db_column='客户姓名')
    e_age = models.IntegerField(db_column='客户年龄')
    e_job = models.CharField(max_length=64, db_column='客户职业', null=True, blank=True)
    province = models.CharField(max_length=32, db_column='客户所在省', null=True, blank=True)
    city = models.CharField(max_length=32, db_column='客户所在市', null=True, blank=True)
    p_name = models.CharField(max_length=64, db_column='项目名称')
    join_time = models.DateTimeField(db_column='加入项目时间')
    update_time = models.DateTimeField(db_column='最近更新时间')
    is_delete = models.BooleanField(default=False, db_column='是否删除')

    class Meta:
        db_table = 'employee'
