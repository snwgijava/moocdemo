from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserProfile(AbstractUser):
    #自定义的性别选择
    GENDER_CHOICES = (('male','男'),('female','女'))
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='')
    #生日可以为空
    birthday = models.DateField(verbose_name='生日',null=True,blank=True)
    #性别 只能男或女，默认女
    gender = models.CharField(max_length=5,verbose_name='性别',choices=GENDER_CHOICES,default='female')
    address = models.CharField(max_length=100,verbose_name='地址',default='')
    #电话可以为空
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name='电话')
    #头像，默认使用default.png
    image = models.ImageField(upload_to='image/%Y/%m',default='image/default.png',max_length=100)

    #Meta信息，后台栏目名
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username