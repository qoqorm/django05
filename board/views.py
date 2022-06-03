from email import message
import re
from django.shortcuts import redirect, render
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.

def index(request):
    kw = request.GET.get("kw", "")
    cate = request.GET.get("cate", "")

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            messages.warning(request, "카테고리가 지정되지 않았습니다.")
            b = Board.objects.all()
    else:
        b = Board.objects.all()

    pg = request.GET.get("page", 1)
    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "kw" : kw,
        "cate" : cate,
    }
    return render(request, "board/index.html", context)

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    r = r.order_by("-pubdate")
    context = {
        "b" : b,
        "rset" : r,
    }
    return render(request, "board/detail.html", context)

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
    else:
        messages.warning(request, "그건 안돼^^ 돌아가^^")
    return redirect("board:index")

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        if request.user:
            Board(subject=s, content=c, writer=request.user, pubdate=timezone.now()).save()
        else:
            pass
        return redirect("board:index")

    return render(request, "board/create.html")

def update(request, bpk):
    b = Board.objects.get(id=bpk)

    if b.writer != request.user:
        messages.error(request, )
        return redirect("board:index")

    if request.method == "POST":
        sb = request.POST.get("sub")
        ct = request.POST.get("con")
        b.subject, b.content = sb, ct
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b" : b
    }
    return render(request, "board/update.html", context)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    p = timezone.now()
    Reply(board=b, replyer=request.user, comment=c, pubdate=p).save()
    return redirect("board:detail", bpk)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        messages.error(request, "^^ 소용없지롱~")
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

    
def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)