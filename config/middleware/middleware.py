#!coding=utf-8

import  traceback
from django.utils.deprecation import MiddlewareMixin

from django import http
# from django.core.urlresolvers import reverse
from django.shortcuts import reverse
from  auth import views as auth_views
from django.conf import settings

logger = settings.GO_LOGGER


class UserAuthMiddleware( MiddlewareMixin ):

    def __init__(self, get_response=None):
        MiddlewareMixin.__init__(self)
        self.get_response = get_response

    def process_request(self, request):
        try:
            full_path = request.path

            #logger.debug(full_path)

            # 允许logo
            if full_path == '/favicon.ico':
                return http.HttpResponseRedirect( '/static/favicon.ico' )

            begin_path = settings.SESSION_COOKIE_PATH
            url_path1 = full_path[len( begin_path ):full_path.rfind(".")]

            # 对非 html 结尾的url进行判断
            if not full_path.endswith(".html") :
                # 对不存在用户登录信息的请求跳转到登录界面
                obj = auth_views.check_is_login( request )
                if obj:
                    ## 判断是否超级用户,超级用户不做权限判断
                    begin_path = settings.SESSION_COOKIE_PATH

                    if not obj.is_superuser :

                        real_path = full_path[len( begin_path ):full_path.rfind(".")]

                        if real_path == "" :
                            return http.HttpResponseRedirect(reverse('home_index_html'))

                        if not auth_views.check_user_has_permission(obj,real_path):
                            return http.HttpResponseForbidden(status=403)
                else :
                    return http.HttpResponseRedirect(reverse('auth_login'))

        except Exception as ex :
            settings.GO_LOGGER.error(traceback.format_exc())


    def process_response(self, request, response):
        return  response