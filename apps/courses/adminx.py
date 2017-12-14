# coding: utf-8
import xadmin

from models import Course, BannerCourse, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums',
                    'image', 'click_nums', 'add_time']
    list_filter = list_display
    search_fields = list_display[:]
    search_fields.remove('add_time')
    ordering = ['-click_nums']
    readonly_fields = ['click_nums', 'students']
    exclude = ['fav_nums']
    style_fields = {'detail': 'ueditor'}

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs.filter(is_banner=False)
        return qs


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums',
                    'image', 'click_nums', 'add_time']
    list_filter = list_display
    search_fields = list_display[:]
    search_fields.remove('add_time')
    ordering = ['-click_nums']
    readonly_fields = ['click_nums', 'students']

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs.filter(is_banner=True)
        return qs


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
