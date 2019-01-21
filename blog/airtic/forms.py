from django import forms
from django.contrib.auth.hashers import check_password

from airtic.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, required=True,
                                error_messages={'required': '用户名必填', 'max_length': '用户名不能超过20字符',
                                                })
    pwd = forms.CharField(max_length=20, required=True,
                          error_messages={'required': '密码必填', 'max_length': '密码不能超过20字符'})
    def clean(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError()
        password = self.cleaned_data.get('pwd')
        if not check_password(password,user.password):
            raise forms.ValidationError()
        return self.cleaned_data
