# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CityDict, CourseOrg, Teacher
from .forms import UserAskForm
from courses.models import Course
from Lighten.settings import PAGINATION_SETTINGS


class OrgView(View):
    """
        课程机构列表功能
    """

    def get(self, request):
        # 取出城市、类别、排序参数
        city_id = request.GET.get('city', '')
        category = request.GET.get('ct', '')
        sort = request.GET.get('sort', '')

        # 机构排名
        hot_orgs = CourseOrg.objects.order_by('-click_nums')[:3]
        # 城市
        all_cities = CityDict.objects.all()
        # 授课教师
        all_teachers = Teacher.objects.all()

        # 根据城市筛选课程机构
        if city_id:
            all_organizations = CourseOrg.objects.filter(city_id=int(city_id))
        else:
            all_organizations = CourseOrg.objects.all()

        # 根据类别筛选课程机构
        if category:
            all_organizations = all_organizations.filter(category=category)

        # 根据sort: 'students' or 'courses'进行排序
        if sort:
            sort_dict = {'students': '-student_nums',
                         'courses': '-course_nums'}
            all_organizations = all_organizations.order_by(sort_dict[sort])

        # 对课程机构进行分页
        per_page = PAGINATION_SETTINGS.get('ORGANIZATION_NUM_PER_PAGE', '5')
        paginator = Paginator(all_organizations, per_page=per_page, request=request)
        try:
            page_num = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            page_num = 1
        # 分页后的课程机构
        org_paginator = paginator.page(page_num)

        return render(request, 'org-list.html',
                      {'org_paginator': org_paginator,
                       'all_cities': all_cities,
                       'org_nums': all_organizations.count(),
                       'cur_city_id': city_id,
                       'category': category,
                       'hot_orgs': hot_orgs,
                       'sort': sort})


class AddUserAskView(View):
    """处理用户'我要学习'表单"""
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}', content_type='application/json')


class OrgDetailHomepageView(View):
    """首页->课程机构->机构首页"""
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {'course_org': course_org,
                                                            'all_courses': all_courses,
                                                            'all_teachers': all_teachers,
                                                            # 用于org_detail_base.html中确定标签的active
                                                            'current_page': 'homepage'})


class OrgDetailCourseView(View):
    """首页->课程机构->机构课程"""
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {'course_org': course_org,
                                                          'all_courses': all_courses,
                                                          'current_page': 'courses'})


class OrgDetailDescView(View):
    """首页->课程机构->机构介绍"""
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {'course_org': course_org,
                                                        'current_page': 'desc'})


class OrgDetailTeacherView(View):
    """首页->课程机构->机构讲师"""
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {'course_org': course_org,
                                                            'all_teachers': all_teachers,
                                                            'current_page': 'teachers'})