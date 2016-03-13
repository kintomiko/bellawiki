# -*- coding:UTF-8 -*-
from django.db import models
import lunar
# Create your models here.

class CharNullField(models.CharField): #subclass the CharField
    description = "CharField that stores NULL but returns ''"
    __metaclass__ = models.SubfieldBase # this ensures to_python will be called
    def to_python(self, value):  #this is the value right out of the db, or an instance
       if isinstance(value, models.CharField): #if an instance, just return the instance
              return value 
       if value==None:   #if the db has a NULL (==None in Python)
              return ""  #convert it into the Django-friendly '' string
       else:
              return value #otherwise, return just the value
    def get_prep_value(self, value):  #catches value right before sending to db
       if value=="":     #if Django tries to save '' string, send the db None (NULL)
            return None
       else:
            return value #otherwise, just pass the value

class LunarableDateField(models.DateField):
    def lunar(self):
        t = lunar.get_lunar_date(self.year, self.month, self.day)
        return (t[1], t[2])

class Tag(models.Model):
    WORK = 301
    FILE = 302
    TAG_TYPES = (
        (WORK, '作品'),
        (FILE, '文件'),
        )
    type = models.IntegerField('类别',choices=TAG_TYPES,
        default=WORK)
    name = models.CharField('标签', max_length=255)
    def __str__(self):
        return self.name.encode("utf8")

class File(models.Model):
    ARTICLE = 101
    PICTURE = 102
    MUSIC = 103
    VIDEO = 104
    FILE_TYPES = (
        (ARTICLE, '文章'),
        (PICTURE, '图片'),
        (MUSIC, '音乐'),
        (VIDEO, '视频'),
    )
    QUALITY_LEVELS = (
        (1, '低'),
        (2, '流畅'),
        (3, '标清'),
        (4, '高清'),
        (5, '无损'),
    )
    type = models.IntegerField('类别',choices=FILE_TYPES,
        default=MUSIC)
    quality = models.IntegerField('质量', choices=QUALITY_LEVELS,
        default=3, blank=True)
    name = models.CharField('文件名', max_length=255)
    desc = models.CharField('描述', max_length=2000, blank=True)
    md5 = CharNullField('md5', max_length=32, unique=True, blank=True)
    url = models.CharField('URL', max_length=2048)
    tags = models.ManyToManyField(Tag, related_name='files', blank=True)
    date = models.DateField('时间', blank=True)
    def __str__(self):
        return self.name.encode("utf8")

class Work(models.Model):
    MUSIC = 201
    INTERVIEW = 202
    ADVERTISE = 203
    ENTERTAIN = 204
    MOVIE = 205
    MAGZINE = 206
    TV = 207
    ACTIVITY = 208
    SKETCH = 209
    COMPETETION = 210
    WORK_TYPES = (
        (MUSIC, '音乐'),
        (INTERVIEW, '访谈'),
        (ADVERTISE, '广告'),
        (ENTERTAIN, '综艺'),
        (MOVIE, '电影'),
        (MAGZINE, '杂志'),
        (TV, '电视'),
        (ACTIVITY, '活动'),
        (SKETCH, '小品'),
	(COMPETETION, '比赛'),
    )
    up = models.IntegerField('赞',default=0)
    date = models.DateField('时间', blank=True)
    type = models.IntegerField('类别',choices=WORK_TYPES,
        default=MUSIC)
    title = models.CharField('标题', max_length=255, unique=True)
    desc = models.CharField('描述', max_length=5000, blank=True)
    files = models.ManyToManyField(File, related_name='works', blank=True)
    tags = models.ManyToManyField(Tag, related_name='works', blank=True)
    def __str__(self):
        return self.title.encode("utf8")
