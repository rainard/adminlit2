from django.db import models

class Permission(models.Model):
    name = models.CharField(u'权限',max_length=50,unique=True )
    url = models.CharField(u'链接',max_length=120 ,unique=True)
    parent_type = models.CharField(u'分类',max_length=20,null=True,blank=True)
    i_class = models.CharField(u'Css',max_length=20,default='fa fa-laptop')
    note = models.CharField(u'备注',max_length=120,blank=True,null=True,default=u"无")


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class UserGroup(models.Model):

    permis = models.ManyToManyField(Permission,verbose_name=u'权限')
    name = models.CharField(u'名称',unique=True,max_length=120)
    note = models.CharField(u'备注',null=True,max_length=250)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

class User(models.Model):
    is_staff = models.BooleanField( u'运维', default=False )
    is_active = models.BooleanField( u'有效', default=True )
    is_superuser = models.BooleanField( u'超级用户', default=False )

    usergroup = models.ForeignKey('UserGroup' ,on_delete=models.PROTECT,verbose_name=u'用户组')
    username = models.CharField(u'用户名',max_length=64,unique=True)
    password = models.CharField(u'密码',max_length=128)
    email = models.EmailField(u'邮箱',null=True)
    first_name = models.CharField(u'姓',null=True,max_length=64)
    last_name = models.CharField(u'名',null=True,max_length=64)
    last_login = models.DateTimeField(u'最后登录',null=True)
    data_joined = models.DateTimeField(u'加入日期',null=True)

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.__unicode__()




