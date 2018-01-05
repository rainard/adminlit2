#coding=utf-8

from django import forms
from .models import *

class ServerRoomForm(forms.ModelForm):
    class Meta:
        model = ServerRoom
        fields = "__all__"
