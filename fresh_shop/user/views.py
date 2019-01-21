from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.forms import RegisterFrom, LoginForm, AddressForm
from user.models import User, UserAddress, Browse


class HttpRespondRedirect(object):
    pass


def register(request):
    if request.method == 'GET':

        return render(request,'register.html')
    if request.method == 'POST':
        # 使用表单做校验
        form = RegisterFrom(request.POST)
        if form.is_valid():
            # 正确
            user = User()
            user.username = form.cleaned_data['user_name']
            print(form.cleaned_data['user_name'])
            print(user.username)
            # user.password = form.cleaned_data['pwd']
            user.email = form.cleaned_data['email']

            user.password = make_password(form.cleaned_data['pwd'])
            user.save()
            return HttpResponseRedirect(reverse('user:login'))

        else:
            errors = form.errors
            return render(request,'register.html',{'errors':errors})

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            username= form.cleaned_data['username']
            user = User.objects.filter(username=username).first()

            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:

            errors = form.errors
            # print(errors)
            return render(request,'login.html',{'errors':errors})
def logout(request):
    if request.method=='GET':
        request.session.flush()
        return HttpResponseRedirect(reverse('goods:index'))


def user_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id).all()
        act3 = 'site'
        return render(request,'user_center_site.html',{'user_address':user_address,'act3':act3})
    if request.method == 'POST':
        form= AddressForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            mobile = form.cleaned_data['mobile']
            postcode = form.cleaned_data['postcode']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(
                signer_name = username,
                address = address,
                signer_mobile = mobile,
                signer_postcode = postcode,
                user_id = user_id,)
            return HttpResponseRedirect(reverse('user:user_site'))
        else:
            errors = form.errors
            return render(request,'user_center_site.html',{'errors':errors})

def user_info(request):
    if request.method == 'GET':
        act1 = 'info'
        user_id = request.session.get('user_id')
        brs = Browse.objects.filter(u_id=user_id)
        if not brs:
            brs = ''
        return render(request,'user_center_info.html',{'act1':act1,'brs':brs})


