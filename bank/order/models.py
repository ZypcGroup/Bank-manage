from django.db import models

# Create your models here.
class User(models.Model):
    uid = models.AutoField(primary_key=True)#方法AutoField用来设置自增字段
    name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    type = models.CharField(max_length=10)
    def __str__(self):
        return self.name
    #self.后边的参数必须是char类型的


class List(models.Model):
    lid = models.AutoField(primary_key=True)
    danger = models.CharField(max_length=255)
    thing = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    money = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    #people = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,blank=True)        不再设置主键
    name = models.CharField(max_length=25)
    #num = models.CharField(max_length=255)
    def __str__(self):
        return self.name

