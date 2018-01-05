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

def time_to_str(datetime_obj):
    import time
    if datetime_obj:
        return time.strftime( '%Y-%m-%d %H:%M:%S', datetime_obj )
    else:
        return time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime( time.time() ) )


def decode_session(key):
    return md5( key + time_to_str( None ) )

def cache_user_session(user,timeout=1296000):
    from django.core.cache import cache
    username = user.username
    session = decode_session(username + user.password )
    cache.set(session,username,timeout=timeout)
    cache.set(username,user,timeout=timeout)
    return session
