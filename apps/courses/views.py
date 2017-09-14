# coding: utf-8

from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.function import order_by_occur_nums
from utils.mixin_utils import LoginRequiredMixin
from Lighten.settings import PAGINATION_SETTINGS


def get_related_courses(request, course):
    """
    根据当前course获取推荐课程(该课程的同学还学过)
    :param   request:                   request对象
    :param   course:                    Course()对象
    :return: relate_courses   (list)    推荐课程
    """

    # 记录用户学习的课程: 关联用户-课程表
    # 查询用户是否已经关联了该课程
    user_course_record = UserCourse.objects.filter(user=request.user, course=course)
    if not user_course_record:
        user_course_record = UserCourse(user=request.user, course=course)
        user_course_record.save()

    # 推荐功能: 该课程的同学还学过..
    # 找出该课程所有记录
    user_coursers = UserCourse.objects.filter(course=course)
    # 获取该课程记录的所有学生
    user_ids = [user_courser.user.id for user_courser in user_coursers]
    # 这些学生的所有课程记录
    all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
    # 取出所有课程id(该课程的同学还学过的所有课程id)
    # 如 [1, 1, 2, 2, 2]
    course_ids = [user_course.course.id for user_course in all_user_courses]
    # 再按照课程id的重复次数进行排序
    course_ids = order_by_occur_nums(course_ids)
    # 按照排序后的课程进行逐个获取, 并依次加入relate_courses
    relate_courses = []
    for relate_course_id in course_ids:
        relate_course = Course.objects.filter(id=relate_course_id).exclude(id=course.id)
        # 取Top5
        if relate_course and len(relate_courses) <= 5:
            relate_courses.append(relate_course[0])
    return relate_courses


class CourseListView(View):
    """课程列表"""

    def get(self, request):
        # 最新公开课
        all_courses = Course.objects.order_by('-add_time').all()
        # 热门课程推荐
        hot_courses = Course.objects.order_by('-click_nums').all()[:3]

        # 课程搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) |
                                             Q(you_need_know__icontains=search_keywords) |
                                             Q(teacher_tell__icontains=search_keywords) |
                                             Q(degree__icontains=search_keywords) |
                                             Q(category__icontains=search_keywords) |
                                             Q(tag__icontains=search_keywords))

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

        return render(request, 'course-list.html', {'hot_courses': hot_courses,
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


class CourseInfoView(LoginRequiredMixin, View):
    """(用户点击开始学习后)课程章节页"""

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 课程推荐(该课的同学还学过)
        relate_courses = get_related_courses(request, course)
        # 课程资源
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {'course': course,
                                                     'course_resources': course_resources,
                                                     'relate_courses': relate_courses})


class CourseCommentView(LoginRequiredMixin, View):
    """课程评论页"""

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course_resources = CourseResource.objects.filter(course=course)
        course_comments = CourseComments.objects.filter(course=course)

        # 课程推荐(该课的同学还学过)
        relate_courses = get_related_courses(request, course)

        return render(request, 'course-comment.html', {'course': course,
                                                       'course_resources': course_resources,
                                                       'course_comments': course_comments,
                                                       'relate_courses': relate_courses})


class AddCommentView(View):
    """ajax 添加评论"""

    def post(self, request):

        # 用户必须为登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}',
                                content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comment', '')
        if course_id > 0 and comment:
            course = Course.objects.get(id=course_id)

            course_comment = CourseComments()
            course_comment.course = course
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}',
                                content_type='application/json')


class CourseVideoView(View):
    """课程视频播放"""

    def get(self, request, video_id):
        # 获取video及其course
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # 记录用户学习的课程: 关联用户-课程表
        # 查询用户是否已经关联了该课程
        user_course_record = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course_record:
            user_course_record = UserCourse(user=request.user, course=course)
            user_course_record.save()

        # 课程推荐(该课的同学还学过)
        relate_courses = get_related_courses(request, course)
        # 课程资源
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-play.html', {'course': course,
                                                    'course_resources': course_resources,
                                                    'relate_courses': relate_courses,
                                                    'video': video})
