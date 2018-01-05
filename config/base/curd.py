# coding=utf-8
import json
import traceback
from datetime import datetime
from datetime import date
from itertools import chain
from django import http
from django.views import View
from django.db.models import Q
from django.conf.urls import url
from django.shortcuts import render
from django.db.models import QuerySet
# from django.forms.models import model_to_dict

def model_to_dict(instance, fields=None, exclude=None):
    """
    Returns a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned dict.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned dict, even if they are listed in
    the ``fields`` argument.
    """
    import pprint
    from django.db import models
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
        # Evaluate ManyToManyField QuerySets to prevent subsequent model
        # alteration of that field from being reflected in the data.
        if isinstance(f, models.ManyToManyField):
            data[f.name] = list(data[f.name])
        if isinstance(f, models.ForeignKey):
            value =  data[f.name]
            try :
                data[f.name] = f.__dict__['related_model'].objects.get(id=data[f.name])
            except Exception as ex :
                data[f.name] = value
    return data

class CJsonEncoder( json.JSONEncoder ):
    def default(self, obj):
        try:
            if isinstance( obj, datetime ):
                return obj.strftime( '%Y-%m-%d %H:%M:%S' )
            elif isinstance( obj, date ):
                return obj.strftime( '%Y-%m-%d' )
            elif isinstance( obj, QuerySet ):
                return None
            else:
                return json.JSONEncoder.default( self, obj )
        except Exception as ex :
            return str(obj)

class retMsg():
    def __init__(self):
        self.msg = u'Success'
        self.success = True

    def to_dict(self):
        return {
            'msg' : self.msg,
            'success' : self.success
        }

class TableData():
    def __init__(self):
        self.prefix = '#'
        self.url_prefix = '#'
        self.prefix_title = None
        self.title = u'List'
        self.page_title = 'List Page'
        self.headers = []
        self.cols = []
        self.show_url = '#'
        self.list_url = '#'
        self.update_url = '#'
        self.add_url = '#'
        self.remove_url = '#'

        self.modelClass = None
        self.modelForm = None

        self.list_template = 'base/table.html'
        self.edit_template = 'base/form.html'

class FormData():
    def __init__(self):
        self.title = u'Edit'
        self.id = None
        self.submit_url = '#'
        self.obj_form = None
        self.msg = None

class CurdModelEntry():
    def __init__(self,table,form):
        self.table = table
        self.form = form

class CurdShow(View):
    entry = None
    def __init__(self,entry,*args,**kwargs):
        super( View, self ).__init__()
        self.entry = entry
        self.args =args
        self.kwargs = kwargs

    def get(self,request,*args,**kwargs):
        return obj_show(request,self.entry.table)

class CurdList(View):
    entry = None
    def __init__(self,entry,*args,**kwargs):
        super( View, self ).__init__()
        self.entry = entry
        self.args =args
        self.kwargs = kwargs

    def get(self,request,*args,**kwargs):
        return obj_list(request,self.entry.table)

class CurdAdd(View):
    entry = None
    def __init__(self,entry,*args,**kwargs):
        super( View, self ).__init__()
        self.entry = entry
        self.args =args
        self.kwargs = kwargs

    def get(self,request,*args,**kwargs):
        return obj_add_get(request,self.entry.table,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return obj_add_post(request,self.entry.table,*args,**kwargs)

class CurdUpdate(View):
    entry = None
    def __init__(self,entry,*args,**kwargs):
        super( View, self ).__init__()
        self.entry = entry
        self.args =args
        self.kwargs = kwargs

    def get(self,request,*args,**kwargs):
        return obj_update_get(request,self.entry.table,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return obj_update_post(request,self.entry.table,*args,**kwargs)


class CurdRemove(View):
    entry = None
    def __init__(self,entry,*args,**kwargs):
        super( View, self ).__init__()
        self.entry = entry
        self.args =args
        self.kwargs = kwargs

    def post(self,request,*args,**kwargs):
        return obj_remove(request,self.entry.table,*args,**kwargs)

def create_table_data(modelClass,modelForm,prefix,url_prefix,*args,**kwargs):
    table = TableData()
    table.prefix = prefix
    table.url_prefix = url_prefix
    table.modelClass = modelClass
    table.modelForm = modelForm
    for key in table.__dict__.keys():
        if key in kwargs:
            table.__setattr__(key,kwargs[key])

    if 'cols' not in kwargs :
        table.cols, table.headers = get_cols_headers_from_modelform( modelClass, modelForm )

    table.show_url ='{0}.html'.format(url_prefix)
    table.list_url ='{0}.list'.format(url_prefix)
    table.update_url = '{0}.update'.format(url_prefix)
    table.add_url ='{0}.add'.format(url_prefix)
    table.remove_url ='{0}.remove'.format(url_prefix)

    return table

def get_cols_headers_from_modelform(objModel,objectForm):
    tmp_headers = []
    tmp_cols = []

    from django.forms.models import ModelFormMetaclass
    if type(objectForm) == ModelFormMetaclass :
        for f in objModel._meta.get_fields():
            try:
                tmp_headers.append( f.verbose_name )
                tmp_cols.append( f.name )
            except Exception as ex:
                pass
    else :
        dics = objectForm.__dict__['declared_fields']
        for key in dics:
            tmp_headers.append( dics[key].label )
            tmp_cols.append( key )
    return tmp_cols,tmp_headers


def __get_search_filter(filter_cols, search_value):
    sql_query = Q()
    sql_query.connector = 'OR'
    for col in filter_cols:
        try:
            sql_query.children.append( (col + '__contains', search_value) )
        except Exception as ex:
            print(traceback.print_exc())
    return sql_query

def create_crud(objModel,objForm,prefix,url_prefix,title,*args,**kwargs):
    table = create_table_data(objModel,objForm,prefix,url_prefix,*args,**kwargs)
    table.title = u'{0} 查看'.format(title)
    table.page_title = title
    table.prefix_title = title
    form = FormData()
    form.title = u'{0} 编辑'.format(title)
    form.submit_url = table.add_url
    entry = CurdModelEntry(table,form)
    return create_urls(entry,*args,**kwargs)

def create_urls(entry,*args,**kwargs):
    table = entry.table
    prefix = table.prefix
    return [
        url(table.show_url,CurdShow.as_view(entry=entry,*args,**kwargs),name='{}_html'.format(prefix)),
        url(table.list_url,CurdList.as_view(entry=entry,*args,**kwargs),name='{}_list'.format(prefix)),
        url(table.update_url,CurdUpdate.as_view(entry=entry,*args,**kwargs),name='{}_update'.format(prefix)),
        url(table.add_url,CurdAdd.as_view(entry=entry,*args,**kwargs),name='{}_add'.format(prefix)),
        url(table.remove_url,CurdRemove.as_view(entry=entry,*args,**kwargs),name='{}_remove'.format(prefix)),
    ]

def obj_show(request,table,msg = None):

    return render( request, table.list_template, {'table': table,'msg':msg} )

def obj_list(request,table):
    modelClass = table.modelClass

    search_value = request.GET.get( 'search', None )
    limit = int( request.GET.get( 'limit', 10 ) )
    start = int( request.GET.get( 'start', 0 ) )
    page = int( (request.GET.get( 'page', 1 )) )

    filter_cols = []
    for field in modelClass._meta.fields:

        from django.db.models.fields import CharField
        if type( field ) == CharField:
            filter_cols.append( field.name )

    total = 0
    json_dic = {}
    objs = None

    if search_value :
        objs = modelClass.objects.filter(__get_search_filter( filter_cols, search_value ))
        total = objs.count()
    else :
        objs = modelClass.objects.all()
        total = objs.count()

    check_start = start
    check_end = start + limit

    json_dic["total"] = total
    json_dic["limit"] = limit
    json_dic["page"] = page
    json_dic["data"] = []

    if check_start > total:
        return http.JsonResponse(json_dic)

    if check_end > total:
        check_end = total

    data = []
    for obj in objs :
        obj_dic = model_to_dict( obj )
        data.append(obj_dic)

    json_dic["data"] = data
    # return http.JsonResponse(json_dic)
    return http.HttpResponse(json.dumps( json_dic, cls=CJsonEncoder ), content_type="application/json")

def obj_add_get(request,table,*args,**kwargs):

    id = request.GET.get('id',-1)
    form_table = FormData()
    form_table.title = u'{0} 编辑'.format( table.prefix_title )
    form_table.submit_url = table.add_url

    try :
        obj = table.modelClass.objects.get(id=id)
        form_table.obj_form = table.modelForm(instance=obj)
    except Exception as ex :
        form_table.obj_form = table.modelForm()

    return render(request,table.edit_template,{'table':form_table})

def obj_add_post(request,table,*args,**kwargs):
    obj_form = table.modelForm(request.POST)
    if obj_form.is_valid() :
        obj_form.save()
        return http.HttpResponseRedirect(table.show_url)

    form_table = FormData()
    form_table.title = u'{0} 编辑'.format( table.prefix_title )
    form_table.submit_url = table.add_url
    form_table.obj_form = obj_form

    return render(request,table.edit_template,{'table':form_table})

def obj_update_get(request,table,*args,**kwargs):
    id = request.GET.get('id',-1)

    resp_msg = retMsg()
    form_table = FormData()
    form_table.submit_url = table.update_url
    form_table.title = u'{0} 更新'.format( table.prefix_title )

    try:
        obj = table.modelClass.objects.get(id=id)
        form_table.obj_form = table.modelForm(instance=obj)
        form_table.id = id
        resp_msg.msg = u'更新完成'
        resp_msg.success = True
    except Exception as ex :
        resp_msg.msg = "{0}".format(ex)
        resp_msg.success = False
        return obj_show(request,table,msg=resp_msg.msg)

    return render( request, table.edit_template, {'table': form_table} )

def obj_update_post(request,table,*args,**kwargs):
    id = request.POST.get('id',-1)
    resp_msg = retMsg()
    form_table = FormData()
    form_table.submit_url = table.update_url
    form_table.title = u'{0} 更新'.format( table.prefix_title )
    try:
        obj = table.modelClass.objects.get( id=id )
        obj_form = table.modelForm(request.POST,instance=obj)
        if obj_form.is_valid():
            obj_form.save()
            return obj_show(request,table,msg=u'更新成功')
        form_table.obj_form = obj_form
    except Exception as ex :
        pass

    return render( request, table.edit_template, {'table': form_table} )

def obj_remove(request,table,*args,**kwargs):
    id = request.POST.get('id',None)
    resp_msg = retMsg()
    try :
        if id :
            obj  = table.modelClass.objects.get(id=id)
            obj.delete()
            resp_msg.success = True
            resp_msg.success = u'删除成功'
        else :
            resp_msg.success = False
            resp_msg.msg = u'错误的ID'
    except Exception as ex :
        resp_msg.success = False
        resp_msg.msg = ex

    return http.JsonResponse(resp_msg.to_dict())