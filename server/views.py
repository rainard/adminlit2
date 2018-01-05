from django.shortcuts import render

from config.base import curd
from .forms import *

BASE_URLS = [ ]

BASE_URLS =  BASE_URLS + curd.create_crud(ServerRoom,ServerRoomForm,'serverroom','server/serverroom',u'机房')

def urls():
    all_urls = BASE_URLS + [  ]
    return all_urls