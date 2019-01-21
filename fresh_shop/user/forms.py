import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterFrom(forms.Form):
    user_name = forms.CharField(max_length=20,min_length=5,
                                required=True,
                                error_messages={'required':'用户名必填','max_length':'用户名不能超过20字符','min_length':'用户名不能小于5字符'})
    pwd = forms.CharField(max_length=20,min_length=8,required=True,
                                error_messages={'required':'密码必填','max_length':'密码不能超过20字符','min_length':'密码不能小于8字符'})

    allow = forms.BooleanField(required=True,
                                error_messages={'required':'必须同意协议'})

    cpwd = forms.CharField(max_length=20,min_length=8,required=True,
                                error_messages={'required':'密码必填','max_length':'密码不能超过20字符','min_length':'密码不能小于8字符'})

    email = forms.CharField(required=True,
                                error_messages={'required':'邮箱必填'})
    def clean_user_name(self):
        # print('zhanhhu')
        username = self.cleaned_data['user_name']
        print(username)
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('账户已存在')
        return self.cleaned_data['user_name']
    def clean(self):
        # print('123')
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd':'密码不一致'})
        return self.cleaned_data
    def clean_email(self):
        email_reg = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        email = self.cleaned_data['email']
        if not re.match(email_reg,email):
            raise forms.ValidationError('邮箱格式错误')
        return self.cleaned_data['email']
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True,
                                error_messages={'required': '用户名必填', 'max_length': '用户名不能超过20字符',
                                                'min_length': '用户名不能小于5字符'})
    pwd = forms.CharField(max_length=20, min_length=8, required=True,
                          error_messages={'required': '密码必填', 'max_length': '密码不能超过20字符', 'min_length': '密码不能小于8字符'})
    def clean(self):
        # print(1)
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            # print(2)
            raise forms.ValidationError({'username':'无该账号'})
        password = self.cleaned_data.get('pwd')
        if not check_password(password,user.password):
        # if password != user.password:
        #     print(3)
            raise forms.ValidationError({'pwd': '密码错误'})
        return self.cleaned_data


class AddressForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True,
                                error_messages={'required': '收件人必填', 'max_length': '不能超过20字符',
                                                'min_length': '不能小于5字符'})
    address = forms.CharField(required=True,
                          error_messages={'required': '地址必填'})
    postcode = forms.CharField(required=True,
                          error_messages={'required': '邮编必填'})
    mobile = forms.CharField(required=True,
                          error_messages={'required': '手机号必填'})



