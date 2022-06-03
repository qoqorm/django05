from django.shortcuts import render
from googletrans import Translator
from googletrans import LANGUAGES


def index2(request):
    trans = Translator()
    context = {
        "ndict" : LANGUAGES,
    }
    if request.method == "POST":
        ipk = request.POST.get("il") # input key
        opk = request.POST.get("ol") # output key
        ipw = request.POST.get("iw") # input word
        tr = trans.translate(ipw, src=ipk, dest=opk) # translation
        trn = tr.text # translated text
#        print(ipw, ipk, opk)
        context.update({
            "ow" : trn,
            "il" : ipk,
            "ol" : opk,
            "iw" : ipw,
        })
    return render(request, "trans/index2.html", context)

def index3(request):
    if request.method == "POST":
        b = request.POST.get("bf")
        s = request.POST.get("fr")
        d = request.POST.get("to")
        print(b, s, d)
    return render(request, "trans/index3.html")

def index(request):
    # print(LANGUAGES)
    context = {
        "ndict" : LANGUAGES
    }
    if request.method == "POST":
        b = request.POST.get("bf")
        s = request.POST.get("fr")
        d = request.POST.get("to")
        
        tra = Translator()
        after = tra.translate(b, src=s, dest=d)
        context.update({
            "af" : after.text,
            "bf" : b,
            "fr" : s,
            "to" : d
        })
    return render(request, "trans/index.html", context)