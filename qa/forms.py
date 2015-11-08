# -*- coding:utf-8 -*-
from django import forms
from django.conf import settings
from models import User
from .models import *
import re
import datetime
from django.forms import ModelForm,TextInput,Textarea,Select
# 引入django-tagging
from tagging.forms import TagField
# -- 问题提交表单 --
class QuestionForm(forms.Form):
	title = forms.CharField(
		widget=forms.TextInput(attrs = {"placeholder" : "您的问题","required" :"required","class":"submit-input"}),
				max_length=100,error_messages={"required": "用户名不能为空",}
							)
	description = forms.CharField(widget=forms.TextInput(attrs = {"placeholder" : "问题简述","required" :"required","class":"submit-input",}),
				max_length=200,error_messages={"required": "请写上简要描述",}
							)
	content = forms.CharField(widget=forms.Textarea(attrs = {"cols":83,}),max_length=10000,error_messages={"required": "请输入问题详情",})

	category = forms.ModelChoiceField(
		queryset = Category.objects.all(),
		# 最上面要显示的内容
		empty_label = "选择问题分类",
		widget = forms.Select(attrs={"required":"required","class":"categories-select",}),
		)
	# 加入标签
	tag = TagField(widget=forms.TextInput(attrs={"class":"hidden"}))
# --用户注册表单 --
class RegForm(forms.Form):
	username = forms.CharField(
		widget = forms.TextInput(attrs={"required":"required","class":"email_user",}),
		label='用户名'
		)
	email = forms.EmailField()
	password = forms.CharField(
		widget = forms.PasswordInput()
		)
# -- 用户登录表单 --
class LoginForm(forms.Form):
	username = forms.CharField(
		widget = forms.TextInput(attrs={"required":"required","class":"email_user",}),
		label='用户名'
		)
	password = forms.CharField(
		widget = forms.PasswordInput(attrs={"required":"required","class":"password_user",}),
		label='密码'
		)
# --回答问题表单 --
class AnswerForm(forms.Form):
	answer_content = forms.CharField(widget=forms.Textarea(attrs = {"cols":83,}),max_length=10000,error_messages={"required": "请输入问题详情",})
	question = forms.CharField(widget=forms.HiddenInput())

# --分类提交表单 --
class CategoryForm(forms.Form):
	category = forms.ModelChoiceField(
		queryset = Category.objects.all(),
		# 最上面要显示的内容
		empty_label = "选择问题分类",
		widget = forms.Select(attrs={"required":"required","class":"select-grey-bg","id":"post_c"}),
		label= None
	)     


















	# tag = forms.CharField(
	# 	widget = forms.TextInput(attrs={"placeholder":"标签(最多输入五个)","class":"submit-input tags-input"})
	# 	)
# class QuestionForm(forms.ModelForm):
# 	class Meta:
# 		model = Question
# 		fields = ('title','description','content','category',)
# 		widgets = {
# 			'title': TextInput(attrs={"placeholder" : "您的问题","required" :"required","class":"submit-input"}),
# 			'description': TextInput(attrs={"placeholder" : "问题简述","required" :"required","class":"submit-input",}),
# 			'content' : Textarea(),
# 			'category' : Select(attrs={"required":"required","class":"categories-select",})
# 		}
# 		max_length = {
# 			'title' : 100,
# 			'description': 200,
# 		}
# 		empty_label = {
# 			'category': u"请选择问题分类",
# 		}

			