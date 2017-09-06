# coding: utf-8
import xadmin

from models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums',
                    'image', 'click_nums', 'add_time']
    list_filter = list_display
    search_fields = list_display[:]
    search_fields.remove('add_time')


class LessonAdmin(object):
    list_display = ['name', 'course', 'add_time']
    list_filter = ['name', 'course__name', 'add_time']
    search_fields = ['name', 'course__name']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    list_filter = ['name', 'lesson__name', 'add_time']
    search_fields = ['name', 'lesson__name']


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'download', 'add_time']
    list_filter = ['name', 'course__name', 'download', 'add_time']
    search_fields = ['name', 'course__name', 'download']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
