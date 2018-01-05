
from django import forms
from .models import *

class PermissionForm( forms.ModelForm ):
    class Meta:
        model = Permission
        fields = '__all__'

class UserGroupForm( forms.ModelForm):
    class Meta:
        model = UserGroup
        fields = '__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['last_login','data_joined']
        widgets = {
            'password' : forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super( UserForm, self ).clean()
        if self.is_valid()  :
            from config.base import utils
            password = str(cleaned_data['password'])
            if len(password ) <= 16 :
                self.instance.password = utils.md5(password)
                cleaned_data['password'] = self.instance.password

            if  cleaned_data.get('data_joined') is None :
                self.instance.data_joined = utils.now()

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField( min_length=2, widget=forms.TextInput( attrs={'placeholder': "Username"} ) )
    password = forms.CharField( min_length=6, widget=forms.PasswordInput( attrs={'placeholder': "Password"} ))
    remember = forms.BooleanField(required=False)



