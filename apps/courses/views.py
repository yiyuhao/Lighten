# coding: utf-8

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from Lighten.settings import PAGINATION_SETTINGS


class CourseListView(View):
    """课程列表"""

    def get(self, request):
        all_courses = Course.objects.order_by('-add_time').all()

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
                                                    'all_courses': all_courses,
                                                    'course_paginator': course_paginator,
                                                    'sort': sort})
