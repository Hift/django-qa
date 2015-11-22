#---coding:utf-8 ---
from django.conf.urls import url
from qa.views import *

urlpatterns = [
	url(r'^$' , index ,name = 'index'),
	# 首页最新，最热，未回答
	url(r'^index_ajax$' , index_ajax , name = "index_ajax"),
	# url(r'^',views.register , name = 'register'),
	url(r'^(?P<question_id>[0-9]+)/$' , detail, name = 'detail'),
	# 注册url
	url(r'^reg' ,reg ,name = 'reg'),
	# 登录url
 	url(r'^login', do_log ,name = 'login'),
	# 注销url
 	url(r'^logout',loginout ,name = 'loginout'),
	# 问题提问url
	url(r'^ask', ask , name = 'ask'),
	# 用户url
	url(r'^usercenter/(?P<username>\w+)' , user_center ,name = 'user_center'),
	# 所有用户
	url(r'^user$' ,user_all , name='user_all'),
	# 提交回答
	url(r'^answer', answer_post, name = 'answer_post'),	
	# 答案列表
	url(r'^useranswer/(?P<username>\w+)',user_answer , name = 'user_answer'),
	# 用户提问的问题列表
	url(r'^userquestion/(?P<username>\w+)',user_question , name = 'user_question'),
	# 查询分类列表
	url(r'^category',category,name="category"),
	# tag列表
	url(r'^tag',tag,name="tag"),
	# vote
	url(r'^vote/(?P<question_id>[0-9]+)/$',vote,name="vote"),
 ]