# coding=utf-8

from pprint import pprint
import logging
from django import http
from django.urls import reverse
from auth.models import OperLogs
from config.base import utils

logger = logging.getLogger( "project" )

class UserAuthMiddleware(object):
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request, *args, **kwargs):
        response = self.get_response(request)
        session = request.session
        user_key = 'user'
        logging.info(request.get_full_path())
        path = request.path
        rpath = path[path.find('/')+1:path.rfind( '.' )]
        logger.info( path )


        # 默认允许的页面
        if rpath in ['login','logout'] :
            return response

        is_login = False
        user = None
        try :
            if user_key not in session.keys():
                http.HttpResponseRedirect(reverse('auth_login'))
            else :
                user = session[user_key]
                if user.is_superuser :
                    is_login = True
                else :
                    urls  = session['urls']
                    if rpath in urls :
                        is_login = True

        except Exception as ex :
            is_login = False

        if is_login :
            if not path.endswith('.html') and not path.endswith(".list")  and not path == '/' :
                logs = OperLogs()
                logs.user = user
                logs.path = request.get_full_path()
                logs.log_datetime = utils.now()

                if request.method == 'GET' :
                    logs.pars = "{}".format(utils.querydict_to_str(request.GET))
                if request.method == 'POST':
                    logs.pars = '{}'.format(utils.querydict_to_str(request.POST))
                    pprint(logs.pars)


                logs.save()

            return response
        else :
            return http.HttpResponseRedirect(reverse('auth_login'))


