from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
#用户信息模型
class UserProfile(AbstractUser):
    #自定义的性别选择
    GENDER_CHOICES = (('male','男'),('female','女'))
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='')
    #生日可以为空
    birthday = models.DateField(verbose_name='生日',null=True,blank=True)
    #性别 只能男或女，默认女
    gender = models.CharField(max_length=6,verbose_name='性别',choices=GENDER_CHOICES,default='female')
    address = models.CharField(max_length=100,verbose_name='地址',default='')
    #电话可以为空
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name='电话')
    #头像，默认使用default.png
    image = models.ImageField(upload_to='image/%Y/%m',default='image/default.png',max_length=100,verbose_name='头像')

    #Meta信息，后台栏目名
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

#邮箱验证码模型
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (('register','注册'),('forget','找回密码'))
    code = models.CharField(max_length=20,verbose_name='验证码')
    #未设置null=True,blank=True ,默认不可为空
    email = models.EmailField(max_length=50,verbose_name='邮箱')
    send_type = models.CharField(choices=SEND_CHOICES,max_length=10,verbose_name='邮件类型')
    #now去掉了（），不然会根据编译时间，而不是根据实例化时间
    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}{1}'.format(self.code,self.email)

#轮播模型
class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    image = models.ImageField(max_length=100,upload_to='banner/%Y/%m',verbose_name='轮播图')
    url = models.URLField(max_length=200,verbose_name='访问地址')
    #轮播图的显示顺序，默认很靠后
    index = models.IntegerField(default=100,verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name