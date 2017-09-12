# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from organization.models import CourseOrg


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
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


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
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
