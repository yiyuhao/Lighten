# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    notice = models.CharField(max_length=300, verbose_name=u'课程公告', default='')
    you_need_know = models.CharField(max_length=300, verbose_name=u'课程须知', default='')
    teacher_tell = models.CharField(max_length=300, verbose_name=u'老师告诉你能学到什么', default='')
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')),
                              max_length=2, verbose_name=u'难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    category = models.CharField(max_length=20, verbose_name=u'课程类别', default=u'计算机技术')
    tag = models.CharField(default='', verbose_name=u'课程标签', max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    @property
    def lesson_nums(self):
        """获取课程章节数"""
        return self.lesson_set.all().count()

    @property
    def learning_user_courses(self):
        """获取该课程下的 用户-课程"""
        return self.usercourse_set.all()

    @property
    def lesson(self):
        """获取课程所有章节"""
        return self.lesson_set.all()


class BannerCourse(Course):
    """轮播课程(与course同一张表, 在xadmin中显示两个管理器方便操作)"""

    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    @property
    def video(self):
        """获取章节所有视频"""
        return self.video_set.all()


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    url = models.CharField(max_length=1000, verbose_name=u'访问地址', default='')
    type = models.CharField(max_length=20, verbose_name=u'文件类型', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'名称')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100,
                                verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
