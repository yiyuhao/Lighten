# coding: utf-8

from django.shortcuts import render
from django.views.generic import View


class CourseListView(View):
    """课程列表"""

    def get(self, request):
        return render(request, 'course-list.html', {'current_page': 'course_list'})
