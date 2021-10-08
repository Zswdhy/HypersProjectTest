from django.db import models

""" 客户 model """


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    eName = models.CharField(max_length=64)
    eAge = models.IntegerField(null=True, blank=True)
    eJob = models.CharField(max_length=64, null=True, blank=True)
    province = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    pName = models.CharField(max_length=64, null=True, blank=True)
    joinTime = models.DateTimeField(auto_now=True, null=True, blank=True)
    updateTime = models.DateTimeField(auto_now=True, null=True, blank=True)
    isDelete = models.BooleanField(default=False)
    isInProject = models.BooleanField(default=False)

    class Meta:
        db_table = 'employee'
        verbose_name = '客户'
        ordering = ["eName", "eAge"]


""" 项目列表 model  """


class ProjectsList(models.Model):
    id = models.AutoField(primary_key=True)
    pName = models.CharField(max_length=64, null=True, blank=True)
    pStartTime = models.DateField(null=True, blank=True)
    pEndTime = models.DateField(null=True, blank=True)
    employee_num = models.IntegerField(null=True, blank=True)
    userId = models.IntegerField(null=True, blank=True)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'project_list'
        verbose_name = '项目列表'


""" 项目详情 model """


class ProjectsDetails(models.Model):
    pdId = models.IntegerField(primary_key=True)  # 项目详情 id 自增 id
    pId = models.ForeignKey('ProjectsList', on_delete=models.CASCADE)  # 外键，项目 id
    pName = models.CharField(max_length=64, null=True, blank=True)
    pIntroduce = models.CharField(max_length=255, null=True, blank=True)
    eId = models.ForeignKey('Employee', on_delete=models.CASCADE)  # 外键，客户 id
    eName = models.CharField(max_length=32, null=True, blank=True)
    eAge = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'project_details'
        verbose_name = '项目详情'
