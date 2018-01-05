#!coding=utf-8


def get_headers_from_model(modelClass):
    '''
    根据model类对象获取对象的字段名，显示名
    :param modelClass:
    :return:
    '''
    cols = []
    headers = []
    for f in modelClass._meta.get_fields():
        try:
            cols.append( f.name )
            headers.append( f.verbose_name )
        except Exception as ex:
            pass
    return headers,cols