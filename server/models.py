from django.db import models

# Create your models here.
class ServerRoom(models.Model):
    name = models.CharField(u'机房',max_length=128)

