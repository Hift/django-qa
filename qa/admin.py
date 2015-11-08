# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
class QuestionAdmin(admin.ModelAdmin):

	list_display = ('title','description','inputtime')

	# 添加富文本编辑器
	class Media:
		js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )
        
admin.site.register(Question,QuestionAdmin)
admin.site.register(User)
admin.site.register(Category)
# admin.site.register(Tag)
admin.site.register(Answer)
