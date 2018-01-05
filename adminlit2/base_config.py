#!coding=utf-8
import platform


dev_config={
    'debug' : True,
    'db_host' : '127.0.0.1',
    'db_name'  : 'adminlit2',
    'db_user' : 'root',
    'db_password' : 'E9%bEb3bcbcF2E8D^D',
    'db_port' : 3306 ,
    'redis_host' : '127.0.0.1',
    'redis_port' : 6379,
    'redis_passwd' : '64978f1dd5fb',
    'redis_db' : 1 ,
    'redis_cron_db' : 3
}

product_config={
    'debug' : True,
    'db_host' : '127.0.0.1',
    'db_name'  : 'adminlit2',
    'db_user' : 'root',
    'db_password' : 'E9%bEb3bcbcF2E8D^D',
    'db_port' : 3306 ,
    'redis_host' : '127.0.0.1',
    'redis_port' : 6379,
    'redis_passwd' : '64978f1dd5fb',
    'redis_db' : 1 ,
    'redis_cron_db' : 3
}

def get_config() :
    plat = platform.platform().lower()
    print("========================{0}==================".format(plat))
    try :
        if plat.find('windows') > -1:
            print( "========================windows==================" )
            return dev_config
        else :
            print( "========================Linux or else==================" )
            return product_config

    except Exception as ex :
        pass
    print( "========================excption config==================" )
    return dev_config
