from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.


def read_user_database(file_path: str) -> dict:
    user_database = {}
    with open(file_path, 'r') as file:
        for line in file:
            username, password, otp = line.strip().split(':')
            user_database[username] = {"password": password, "dynamic_password": otp}
    return user_database


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        otp = request.POST.get('otp')

        user_database = read_user_database("user1.txt")

        if username in user_database:
            user_info = user_database[username]
            if user_info["password"] == password and user_info["dynamic_password"] == otp:
                # 使用reverse函数生成URL并重定向
                return redirect('access')
            else:
                messages.error(request, 'Wrong password or dynamic password.!')
                # 重定向到登录页面，使用reverse生成带斜杠的URL
                return redirect('login')
        else:
            messages.error(request, 'Wrong username!')
            # 重定向到登录页面，使用reverse生成带斜杠的URL
            return redirect('login')
    return render(request, 'login.html')


def access(request):
    return render(request, 'access.html')


def fail(request):
    return render(request, 'login.html')
