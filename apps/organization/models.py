# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    in_a_word = models.CharField(max_length=20, verbose_name=u'一句话展示', default=u'')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(max_length=20, verbose_name=u'机构类别', default='train_org',
                                choices=(('pxjg', '培训机构'),
                                         ('gr', '个人'),
                                         ('gx', '高校')))
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'封面图')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')
    student_nums = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    @property
    def teacher_nums(self):
        """获取机构讲师数"""
        return self.teacher_set.all().count()


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'教师名')
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    age = models.IntegerField(default=0, verbose_name=u'年龄')
    academic_degree = models.CharField(max_length=20, verbose_name=u'学位', default=u'本科')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u'头像', default='')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{name} ({org})'.format(name=self.name, org=self.org)

    @property
    def hot_course(self):
        hot_course = self.course_set.order_by('-students')[:1]
        if hot_course:
            return hot_course[0]
        else:
            return None

    @property
    def course_nums(self):
        return self.course_set.count()
