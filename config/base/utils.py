#coding=utf-8

def now():
    import time
    return time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime( time.time() ) )

def md5(src):
    import hashlib
    base_key = '8180x+&pa!a_45m_x-w5bv5&g9&3dxemuf%o7#8&oiua958_sc'
    m2 = hashlib.md5()
    value = "{0}{1}".format( src, base_key )
    m2.update( value.encode( 'utf-8' ) )
    return m2.hexdigest()

def time_to_str(datetime_obj=None):
    import time
    if datetime_obj:
        return time.strftime( '%Y-%m-%d %H:%M:%S', datetime_obj )
    else:
        return time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime( time.time() ) )


def decode_session(key):
    return md5( key + time_to_str(  ) )

def querydict_to_str(query_dict):
    result = ""
    for key in query_dict :
        if key == 'csrfmiddlewaretoken' :
            continue
        result = "{0}={1}<br>{2}".format(key,query_dict.get(key),result)

    return result




