from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "acc/index.html")

def userlogin(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        user = authenticate(username=un, password=up)
        if user:
            login(request, user)
            return redirect("acc:index")
        else:
            messages.error(request, "일치하는 계정이 존재하지 않습니다!")
    return render(request, "acc/login.html")

def signup(request):
    if request.method == "POST":
        una = request.POST.get("uname")
        upa = request.POST.get("upass")
        ucm = request.POST.get("ucomm")
        upi = request.FILES.get("upic")
        try:
            User.objects.create_user(username=una, password=upa, comment=ucm, pic=upi)
            return redirect("acc:login")
        except:
            messages.error(request, "이미 존재하는 사용자입니다.")
        return redirect("acc:login")

    return render(request, 'acc/signup.html')

def userlogout(request):
    logout(request)
    return redirect("acc:index")

def profile(request):
    return render(request, 'acc/profile.html')

def delete(request):
    ck = request.POST.get("pwk")
    if check_password(ck, request.user.password):
        request.user.pic.delete()
        request.user.delete()
        return redirect("acc:index")
    else:
        messages.error(request, "비밀번호가 맞지 않습니다")
        return redirect("acc:profile")

def update(request):
    if request.method == "POST":
        u = request.user
        up = request.POST.get("upass")
        um = request.POST.get("umail")
        uc = request.POST.get("ucomm")
        pi = request.FILES.get("upic")
        if up:
            u.set_password(up)
        u.email = um
        u.comment = uc
        if pi:
            u.pic.delete()
            u.pic = pi
        u.save()
        login(request, u)
        return redirect("acc:profile")
        
    return render(request, "acc/update.html")
