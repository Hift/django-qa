# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# 引入tagging
from tagging.fields import TagField

# 用户模型，继承自AbstractUser
class User(AbstractUser):
	qq = models.CharField(u'QQ',max_length = 20,null=True,blank=True,)
	tel = models.CharField(u'手机',max_length = 11,null=True,blank=True,unique=True)
	avatar = models.FileField(upload_to='avatar/%Y/%m',default='avatar/default.png',max_length = 200,null=True,blank=True,verbose_name='头像')
	class Meta:
		verbose_name = '用户'
		verbose_name_plural = verbose_name
		# 按照id进行倒序排列
		ordering = ['-id']
			
	def __unicode__(self):
		return self.username

#定义问题分类
class Category(models.Model):
	name = models.CharField(max_length=30,verbose_name='分类名称')
	order = models.IntegerField(verbose_name='排序(从小到大）',default=999)
	
	class Meta:
		verbose_name = '问题分类'
		verbose_name_plural = verbose_name
		# 按照order进行顺序排列
		ordering = ['order' , 'id']

	def __unicode__(self):
		return self.name	

# #定义问题标签
# class Tag(models.Model):
# 	name = models.CharField(max_length=30,verbose_name='标签名称')

# 	class Meta:
# 		verbose_name = '标签'
# 		verbose_name_plural = verbose_name
# 		# 按照order进行顺序排列
# 		ordering = [ 'id']
	
# 	def __unicode__(self):
# 		return self.name	

# 定义问题
class Question(models.Model):
	# user与User模型用ForeignKey进行关联
	user = models.ForeignKey(User,verbose_name='用户',null=True)
	title = models.CharField(verbose_name='问题标题', max_length=200)
	# user与Category模型用ForeignKey进行关联
	category = models.ForeignKey(Category,blank=True,null=True,verbose_name='问题分类')
	description = models.CharField(verbose_name='简要描述',max_length = 200)
	content = models.TextField(verbose_name='内容',max_length = 10000)
	inputtime = models.DateTimeField(verbose_name='发布时间',auto_now_add=True)
	# 标签是ManyToManyField关系
	# tag = models.ManyToManyField(Tag,verbose_name='问题标签')
	votes = models.IntegerField(verbose_name='票数',default=0)

	tags = TagField()
	

	class Meta:
		verbose_name = '问题'
		verbose_name_plural = verbose_name
		# 按照id进行倒序排列
		ordering = ['-inputtime']

	def __unicode__(self):
		return self.title



# 评论
class Answer(models.Model):
	user = models.ForeignKey(User,verbose_name='评论用户')
	question = models.ForeignKey(Question,verbose_name='问题')
	answer_content = models.TextField(verbose_name='回答',max_length = 10000)
	answer_time = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)
	pid = models.ForeignKey('self',blank=True,null=True,verbose_name='父级评论')

	class Meta:
		verbose_name = '回答'
		verbose_name_plural = verbose_name
	def __unicode__(self):
		return self.answer_content




class Choice(models.Model):
	#使用ForeignKey对Choice和Question进行一对一绑定
	question = models.ForeignKey(Question)
	c_text = models.CharField(max_length =200)
	vote = models.IntegerField(default=0)




