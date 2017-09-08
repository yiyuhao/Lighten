# coding: utf-8
from django.shortcuts import render

from django.views.generic import View

from .models import CityDict, CourseOrg, Teacher

class OrgView(View):
    """
        课程机构列表功能
    """

    def get(self, request):
        # 课程机构
        all_organizations = CourseOrg.objects.all()
        org_nums = all_organizations.count()
        # 城市
        all_cities = CityDict.objects.all()
        # 授课教师
        all_teachers = Teacher.objects.all()

        return render(request, 'org-list.html',
                      {'all_organizations': all_organizations,
                       'all_cities': all_cities,
                       'org_nums': org_nums})
