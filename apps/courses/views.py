# coding: utf-8

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course
from operation.models import UserFavorite
from Lighten.settings import PAGINATION_SETTINGS


class CourseListView(View):
    """课程列表"""

    def get(self, request):
        # 最新公开课
        all_courses = Course.objects.order_by('-add_time').all()
        # 热门课程推荐
        hot_courses = Course.objects.order_by('-click_nums').all()[:3]

        sort = request.GET.get('sort', '')

        # 根据sort: 'students' or 'courses'进行排序
        if sort:
            sort_dict = {'students': '-students',
                         'hot': '-click_nums'}
            all_courses = all_courses.order_by(sort_dict[sort])

        # 对所有课程进行分页
        per_page = PAGINATION_SETTINGS.get('COURSE_NUM_PER_PAGE', 6)
        paginator = Paginator(all_courses, per_page, request=request)
        try:
            per_page = int(request.GET.get('page', 1))
        except PageNotAnInteger:
            per_page = 1
        # 分页后的课程机构
        course_paginator = paginator.page(per_page)

        return render(request, 'course-list.html', {'current_page': 'course_list',
                                                    'hot_courses': hot_courses,
                                                    'course_paginator': course_paginator,
                                                    'sort': sort})


class CourseDetailView(View):
    """课程详情页"""

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 课程点击数+1
        course.click_nums += 1
        course.save()

        # 获取该课程的收藏状态
        logined = request.user.is_authenticated()
        course_has_fav = True if logined and UserFavorite.objects.filter(user=request.user,
                                                                         fav_id=course.id,
                                                                         fav_type=1) else False
        # 获取该课程机构的收藏状态
        org_has_fav = True if logined and UserFavorite.objects.filter(user=request.user,
                                                                      fav_id=course.course_org.id,
                                                                      fav_type=2) else False
        # 获取tag相同的最高点击课程(作为相关课程推荐)
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag).exclude(id=course.id).order_by('-click_nums')[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {'course': course,
                                                      'relate_courses': relate_courses,
                                                      'course_has_fav': course_has_fav,
                                                      'org_has_fav': org_has_fav})
