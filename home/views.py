from django.shortcuts import render
from django.shortcuts import reverse
from django.conf.urls import url
from django import http
from django.core.cache import cache
import logging

logger = logging.getLogger( "project" )

def urls():
    urlpatterns = [
        url(r'^$',index,name='home_index'),
        url(r'^logout.html',logout,name='home_logout'),

    ]
    return urlpatterns

class IndexMenuButton():
    def __init__(self,name,url,i_class= 'fa  fa-caret-right'):
        self.name = name
        self.url = url
        self.i_class = i_class

class IndexMenuButtonGroup():
    def __init__(self,name,apps,i_class='fa fa-laptop'):
        self.name = name
        self.i_class = i_class
        self.apps = apps

class IndexTable():
    login_url = None
    logout_url = None
    modify_url = None
    def __init__(self,title,app_groups,user):
        self.title = title
        self.app_groups = app_groups
        self.user = user

# 将权限转换成菜单列表
def menu(data):
    clean_menu = []
    mydic = {}
    mydic_class = {}
    for p in data:
        if p.parent_type:
            mydic.setdefault( p.parent_type, [] ).append( p )
            mydic_class[p.parent_type] = p.i_class

    for k in mydic:
        app_list = []
        for obj in mydic[k]:
            tpl_app1 = IndexMenuButton( obj.name,obj.url )
            app_list.append( tpl_app1 )
        tpl_app_group = IndexMenuButtonGroup( k, app_list ,mydic_class[k])
        clean_menu.append( tpl_app_group )

    return clean_menu




def index(request):
    user_obj = request.session.get( 'user',None )

    login_url = reverse('auth_login')

    if not user_obj :
        return http.HttpResponseRedirect(login_url)

    if not user_obj :
        return http.HttpResponseRedirect( login_url )

    permissions = None
    if user_obj.is_superuser :
        from auth.models import Permission
        permissions = Permission.objects.all()
    else :
        permissions = user_obj.usergroup.permis.all()

    group_list = menu( permissions )
    tpl_index_table = IndexTable( u'WeHotel DevOps', group_list, None )
    tpl_index_table.login_url = login_url
    tpl_index_table.user = user_obj
    tpl_index_table.logout_url = reverse('home_logout')

    return render( request, 'home/index.html', {"tpl_obj": tpl_index_table} )

def logout(request):

    session = request.session

    if 'user' in session.keys():
        del request.session['user']

    login_url = reverse( 'auth_login' )
    return http.HttpResponseRedirect(login_url)

