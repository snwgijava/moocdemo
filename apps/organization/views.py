from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
#课程机构列表
from organization.models import CourseOrg, CityDict


class OrgView(View):
    def get(self,request):
        context = {}
        #取得所有课程机构
        all_orgs = CourseOrg.objects.all()
        #取得所有城市
        all_citys = CityDict.objects.all()

        #取出筛选的城市，默认为空
        city_id = request.GET.get('city','')
        #如果选择了某个城市，说明前端传过来值了
        if city_id:
            #在机构中做进一步筛选
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #类别筛选
        category = request.GET.get('ct','')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 总共有多少家机构使用count进行统计
        org_nums = all_orgs.count()

        #热门机构
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        #进行排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        #从所有数据库取出5条，每页显示5条数据
        p = Paginator(all_orgs,5,request=request)
        orgs = p.page(page)
        context['all_orgs'] = orgs
        context['all_citys'] = all_citys
        context['org_nums'] = org_nums
        context['city_id'] = city_id #将city_id传回html,这样可以知道哪个是选中的
        context['category'] = category
        context['hot_orgs'] = hot_orgs
        return render(request,'org-list.html',context)

