from email import message
from django.shortcuts import redirect, render
from .models import Topic, Choice
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def index(request):
    t = Topic.objects.all()
    t = t.order_by("-pubdate")
    context = {
        "tset" : t,
    }
    return render(request, "vote/index.html", context)

def detail(request, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        "t" : t,
        "cset" : c,
    }
    return render(request, "vote/detail.html", context)

def vote(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        cpk = request.POST.get("cho")
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)
    return redirect("vote:detail", tpk)

def cancel(request, tpk):
    u = request.user
    t = Topic.objects.get(id=tpk)
    if u in t.voter.all():
        t.vote.remove(u)
        u.choice_set.get(topic=t).choicer.remove(u)
    return redirect("vote:detail", tpk)

def create(request):
    if request.method == "POST":
        ttl = request.POST.get("ttl")
        tcom = request.POST.get("tcom")      
        cho = request.POST.getlist("cho")
        img = request.FILES.getlist("imgcho")
        comcho = request.POST.getlist("comcho")
#        print(ttl, tcom, cho, img, comcho)
        t = Topic(subject=ttl, maker=request.user, content=tcom, pubdate=timezone.now())
        t.save()

        for na, co, pi in zip(cho, comcho, img):
            Choice(topic=t, name=na, con=co, pic=pi).save()
        return redirect("vote:index")

    return render(request, "vote/create.html")

def delete(request, tpk):
    t = Topic.objects.get(id=tpk)
    if t.maker == request.user:
        cset = t.choice_set.all()
        for i in cset:
            i.pic.delete()
        t.delete()
    else:
        messages.warning(request, "안돼^^ 돌아가^^")
    return redirect("vote:index", tpk)