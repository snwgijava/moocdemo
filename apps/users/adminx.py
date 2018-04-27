__author__ = 'yangjian'
__date__ = '2018/4/27 16:29'

import xadmin

from .models import EmailVerifyRecord,Banner

#创建Email的管理类，不再继承admin
class EmailVerifyRecordAdmin(object):
    #列表
    list_display = ['code','email','send_type','send_time']
    #搜索
    search_fields = ['code', 'email', 'send_type']
    #筛选
    list_filter = ['code','email','send_type','send_time']

class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)

