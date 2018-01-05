
from django import http
from django.shortcuts import render

from django.conf.urls import url
from config.base import curd
from .forms import *

BASE_URLS = [ ]

BASE_URLS =  BASE_URLS + curd.create_crud(Permission,PermissionForm,'permission','auth/permission',u'权限')
BASE_URLS =  BASE_URLS + curd.create_crud(User,UserForm,'user','auth/user',u'用户')
BASE_URLS =  BASE_URLS + curd.create_crud(UserGroup,UserGroupForm,'usergroup','auth/usergroup',u'用户组')

def urls():
    all_urls = BASE_URLS + [
        url(r'^login.html',login_html,name='auth_login'),
        url(r'^login.action',login_action,name='auth_login_action'),
    ]
    return all_urls

def login_html(request,msg=None):
    form = LoginForm()
    return render(request,'auth/login.html',{'form':form,'title':u'登录','msg':msg})

def login_action(request):
    from config.base import utils
    from django.shortcuts import reverse
    form  = LoginForm(request.POST)
    response = None
    if form.is_valid():
        clean_data = form.cleaned_data
        password = clean_data['password']
        username = clean_data['username']
        remember = clean_data['remember']
        md5_password = utils.md5(password)
        try :
            obj = User.objects.filter(password=md5_password,username=username).last()
            obj.last_login = utils.now()
            obj.save()
            session = utils.cache_user_session(obj)
            response = http.HttpResponseRedirect( reverse( 'home_index' ) )
            response.set_cookie('session',session,1296000)
        except Exception as ex :
            response = login_html(request,msg=u'登录失败，错误的用户或密码')

    return response


