from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import UserSelf

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user = request.POST['user']
        password = request.POST['password']
        # 验证用户名和密码，通过的话，返回User对象
        user = auth.authenticate(username=user, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'msg':'Oh!请再检查一下您输入的用户名及密码,他们似乎有些错误!','type':'warning'})


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    if request.method == 'POST':
        userName = request.POST['a']
        realName = request.POST['b']
        passWord = request.POST['c']
        passWordAgain = request.POST['d']
        anoahName = request.POST['e']
        aeduName = request.POST['f']
        aeduPassword = request.POST['g']
        same_name_user = UserSelf.objects.filter(userName=userName)
        if same_name_user:
            return render(request, 'signin.html', {'msg':'用户已经存在，请重新选择用户名！','type':'danger'})
        if passWord == passWordAgain:
            try:
                auth.models.User.objects.create_user(username=userName, password=passWord)
                new_user = UserSelf.objects.create()
                new_user.userName=userName
                new_user.realName=realName
                new_user.anoahName=anoahName
                new_user.aeduName=aeduName
                new_user.aeduPassword=aeduPassword
                new_user.passWord=passWord
                new_user.save()
                return render(request, 'login.html', {'msg':'注册成功,请登录!','type': 'success'})
            except:
                return render(request, 'signin.html', {'msg':'发生了未知的错误!', 'type':'danger'})
        else:
            return render(request, 'signin.html', {'msg':'两次输入的密码不同！','type':'warning'})

def logout(request):
    auth.logout(request)
    return redirect('/')