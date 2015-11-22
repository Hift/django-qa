#--coding:utf-8--
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import *
from forms import *
from django import forms
from time import gmtime, strftime
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
# --tagging--
from tagging.models import Tag,TaggedItem
import hashlib
def global_setting(req):
	SITE_URL = settings.SITE_URL
	MEDIA_URL = settings.MEDIA_URL
 	# 所有问题的计数
 	question_count = Question.objects.all().count()
 	# 所有答案的计数
 	user_count = User.objects.all().count()
 	# category查询表单
	category_Form = CategoryForm()
 	return locals()
# @csrf_exempt
# def index(req):
# 	
# 	# 从客户端获取categoryname
# 	category_name =req.POST.get("name",'')
# 	if category_name:
# 		category = Category.objects.get(name=category_name)
# 		question_category_list = Question.objects.filter(category=category).order_by('-inputtime')[:15]
# 		# question_category_list = getPage(req,question_category_list)
# 		print question_category_list
# 		return render(req,"qa/category_ajax.html",locals())
		
# 	else:
# 		# 最新问题列表
# 		latest_question_list = Question.objects.order_by('-inputtime')[:15]
# 		# latest_question_list = getPage(req,latest_question_list)
# 		return render(req,"qa/index.html",locals())
@csrf_exempt
def index(
        request,
        template='qa/index.html',
        page_template='qa/index_ajax.html',
        extra_context = None):
    context = {
        'latest_question_list': Question.objects.order_by('-inputtime').all(),
        'page_template': page_template,
    }

    # 从客户端接受来的ajax请求
    # category_name = request.POST.get("name",'')
    # if category_name:
    # 	category = Category.objects.get(name=category_name)
    # 	extra_context = {
    # 		'latest_question_list' : Question.objects.filter(category=category).order_by('-inputtime').all(),
    # 	}
    # 	context.update(extra_context)
    if request.is_ajax():
        template = page_template
    return render_to_response(
        template, context, context_instance=RequestContext(request))	

# -----首页最新，最热，未回答-----
@csrf_exempt
def index_ajax(req):
	if req.GET.get('hot'):
		latest_question_list = Question.objects.order_by('-votes').all()
	elif req.GET.get('unanswer'):
		user = req.user
		latest_question_list = Question.objects.exclude(answer__user = user).all()
		# latest_question_list = Question.objects.order_by('-inputtime').all()
	else:
		latest_question_list = Question.objects.order_by('-inputtime').all()
	return render(req,"qa/index_ajax.html",locals())


@csrf_exempt
def category(
        request,
        template='qa/category.html',
        page_template='qa/category_ajax.html',
        extra_context = None):
	category = Category.objects.get(name=request.GET.get('name'))
	context = {
        'question_category_list': Question.objects.filter(category=category),
        'page_template': page_template,
        'category' : category,
    }

	if request.is_ajax():
		template = page_template
	return render_to_response(
        template, context, context_instance=RequestContext(request))	

# # -----栏目分类页面-----
# def category(req):
# 	category = Category.objects.get(name=req.GET.get('name'))
# 	question_category_list = Question.objects.filter(category=category)
# 	if req.is_ajax():
# 		return render(req,"qa/category_ajax.html",locals())
# 	else:
# 		return render(req,"qa/category.html",locals())

# -----栏目分类页面-----
def tag(req):
	tag = Tag.objects.get(name=req.GET.get('name'))
	question_category_list = TaggedItem.objects.get_by_model(Question, tag)
	if req.is_ajax():
		return render(req,"qa/category_ajax.html",locals())
	else:
		return render(req,"qa/category.html",locals())

# -----投票功能实现-----
def vote(req,question_id):
	inputtime = Question.objects.get(id=question_id).inputtime
	hash_id = hashlib.sha1(str(inputtime)).hexdigest()
	if hash_id in str(req.COOKIES.get(question_id)):
		return HttpResponse('您已投票')
	else:
		question = get_object_or_404(Question,pk=question_id)
		if req.GET.get('down'):
			question_vote = question.votes - 1
		else:
			question_vote = question.votes + 1
		question.votes = question_vote
		question.save()
		res = HttpResponse(question_vote)
		res.set_cookie(question_id,value=hash_id)
		return res
# -----提问问题页面-----
def ask(req):
	if req.method == 'POST':
		question_Form = QuestionForm(req.POST)
		if question_Form.is_valid():
			question = Question.objects.create(	title = question_Form.cleaned_data['title'],
												description = question_Form.cleaned_data['description'],
												content = question_Form.cleaned_data['content'],
												inputtime = strftime("%Y-%m-%d %H:%M:%S", gmtime()),
												category = question_Form.cleaned_data['category'],
												tags = question_Form.cleaned_data['tag'],
												# 判断是否用户登录了
												user = req.user if req.user.is_authenticated() else None,											
											)
			
			question.save()
			user = User.objects.get(username=req.user)
			user.points += 5
			user.save()

			return HttpResponseRedirect('/')
	else:
		question_Form = QuestionForm()
	return render(req,"qa/ask.html",locals())

# -----问题详情页-----
def detail(req,question_id):
	id = question_id
	question = Question.objects.get(pk=id)
	answer_Form = AnswerForm({'question': id})
	# 获取答案
	answer_all = Answer.objects.filter(question=question).order_by('id')
	answer_count = answer_all.count()
	answer_list = []
	for answer in answer_all:		
		for item in answer_list:
			# hasattr 用来判断某一对象是否有某一属性
			if not hasattr(item,'children_answer'):
				setattr(item,'children_answer',[])
			if answer.pid == item:
				item.children_answer.append(answer)
				break
		# 如果是父级，直接添加到答案列表
		if answer.pid is None:
			answer_list.append(answer)

	return render(req, 'qa/detail.html', locals())

# -----所有用户-----
def user_all(req):
	user_all = User.objects.all()
	return render(req,'qa/user.html',locals())


# -----用户中心-----
def user_center(req,username):
	question_user = User.objects.get(username=username)
	user_question_list = Question.objects.filter(user__exact = question_user)
	# 用户问题数的计数
	user_question_count = Question.objects.filter(user__exact = question_user).count()
	# 问题答案数的计数
	user_answer_count = Answer.objects.filter(user__exact = question_user).count()
	return render(req,'qa/usercenter.html',locals())

# -----答案列表-----
def user_answer(req,username):
	answer_user = User.objects.get(username=username)
	user_answer_list = Answer.objects.filter(user__exact=answer_user)
	return render(req, 'qa/useranswer.html', locals())

# -----问题列表-----
def user_question(req,username):
	question_user = User.objects.get(username=username)
	user_question_list = Question.objects.filter(user__exact = question_user)
	return render(req,'qa/userquestion.html',locals())
# -----提交答案-----
def answer_post(req):
	answer_Form = AnswerForm(req.POST)
	if answer_Form.is_valid():
		answer = Answer.objects.create( answer_content = answer_Form.cleaned_data['answer_content'],
										question_id = answer_Form.cleaned_data['question'],
										user = req.user if req.user.is_authenticated() else None,
										answer_time = strftime("%Y-%m-%d %H:%M:%S", gmtime()),
			)
		answer.save()
		user = User.objects.get(username=req.user)
		user.points += 5
		user.save()
	return redirect(req.META['HTTP_REFERER'])

# -- 用户注销 --
def loginout(req):
	logout(req)
	return redirect(req.META['HTTP_REFERER'])
# -----用户注册-----

def reg(req):
	if req.method == 'POST':
		reg_Form = RegForm(req.POST)
		if reg_Form.is_valid():
			user = User.objects.create(	username = reg_Form.cleaned_data['username'],
										email = reg_Form.cleaned_data['email'],
										password = make_password(reg_Form.cleaned_data['password']),
									)
			user.save()
			# 登录验证方式，使用django自带
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(req,user)
			return HttpResponseRedirect('/')
		else:
			return render(req, 'qa/failure.html', {'reason': reg_Form.errors})
	else:
		reg_Form = RegForm()
	return render(req, 'qa/register.html',locals())
# -----用户登录-----
def do_log(req):
	if req.method == 'POST':
		login_Form = LoginForm(req.POST)
		if login_Form.is_valid():
			username = login_Form.cleaned_data['username']
			password = login_Form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
				login(req, user)
			else:
				return render(req, 'qa/failure.html', {'reason': '登录验证失败'})
			return HttpResponseRedirect('/')
	else:
		login_Form = LoginForm()
	return render(req, 'qa/login.html',locals())



# # -----分页函数-----
# def getPage(req,question_list):
# 	paginator = Paginator(question_list,2)
# 	print paginator.page_range
# 	try: 	
# 		# 获取客户端提交来的数字
# 		page = req.GET.get('page',1)
# 		page_list = paginator.page(page)

# 	except (EmptyPage,InvalidPage,PageNotAnInteger):
# 		page_list = paginator.page(1)
# 	return page_list
# 问题表单提交
# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['title','description','content']

# def postQuestion(req):
# 	if req.method == "POST":
# 		uf = QuestionForm(req.POST,req.FILES)
# 		if uf.is_valid():
# 			title = uf.cleaned_data['title']
# 			description = uf.cleaned_data['description']
# 			content = uf.cleaned_data['content']
# 			Question.objects.create(title = title , description = description , content = content)
# 			return HttpResponse('ok')
# 	else:
# 		uf = QuestionForm()
# 	return render(req ,'qa/left.html',locals())
"""
def index(req):
	latest_list = Question.objects.order_by('inputtime')[:5]
	#------------------------登录成功之后获取用户名------------------------
	username = req.COOKIES.get('username','')
	context = {
		'latest_list':latest_list,
		'username':username,
		}
	return render(req,"qa/index.html",context)

def vote(req,question_id):
	p = get_object_or_404(Question,pk = question_id)
	try:
		# 此处的choice为detail表单上提交上来的
		selected_choice = p.choice_set.get(pk = req.POST['choice'])
	except(KeyError , Choice.DoesNotExist):
	 	return render(req,'qa/detail.html',{
	 		'question':p,
	 		'error_message=' : 'oh ,No',
	 		})
	else:
		selected_choice.vote += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('qa:results', args = (p.id,)))
def results(req,question_id):
	question = get_object_or_404(Question,pk = question_id)
	return render(req, 'qa/results.html', {'question' : question})
#------------------------注册页面------------------------
class UserForm(forms.Form):
	username = forms.CharField(label='用户名',widget = forms.TextInput(attrs ={'class':'form-control','placeholder':'用户名'}))
	password = forms.CharField(label='密码',widget = forms.PasswordInput(attrs ={'class':'form-control','placeholder':'请输入密码'}))


def register(req):
	#判断POSt
	if req.method == "POST":
		uf = UserForm(req.POST,req.FILES)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			#userimg = uf.cleaned_data['userimg']
			'''
			print uf.cleaned_data['username']
			print uf.cleaned_data['userimg'].name
			print uf.cleaned_data['userimg'].size
			user = User()
			user.username = username
			user.userimg = userimg
			user.save()
			# print req.FILES
			'''
			User.objects.create(username = username , password = password )

			return HttpResponse('ok')
	else:
		uf = UserForm()
	return render(req,"qa/register.html",{'uf':uf})
#------------------------用户登录------------------------
def login(req):
	if req.method == 'POST':
		uf = UserForm(req.POST)
		if uf.is_valid():
			#获取用户、密码
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			#获取的表单数据与数据库进行比较
			user = User.objects.filter(username__exact = username,password__exact = password)
			if user:
				#比较成功跳转index
				response = HttpResponseRedirect('/qa/')
				#将username写入浏览器cookie，失效时间为3600
				response.set_cookie('username',username,3600)
				return response
			else:
				#比较失败
				return HttpResponseRedirect('/qa/login/')
	else:
		uf = UserForm()
	return render_to_response('qa/login.html',{'uf':uf},context_instance=RequestContext(req))
#------------------------退出------------------------
def logout(req):
	response = HttpResponse('logout!!!')
	#清理cookie里保存的username
	response.delete_cookie('username')
	return response

#用户登录后填写表单的地方
#使用ModelForm直接从模型创建表单
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['q_title','q_description','q_content']
    def __unicode__(self):
    	return self.name
def postQuestion(req):
	pass
"""