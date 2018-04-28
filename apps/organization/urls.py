__author__ = 'yangjian'
__date__ = '2018/4/28 21:44'

from django.urls import path


from . import views

urlpatterns = [
    path('org_list/',views.OrgView.as_view(),name='org_list'),
]