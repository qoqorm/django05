from django.shortcuts import render
import speech_recognition as sr
from gtts import gTTS
import os
import time

# Create your views here.
def index(request):
    context = {

    }
    if request.method == "POST":
        txt = request.POST.get("iw")
        tts = gTTS(text=txt, lang='ko')
        filename = request.POST.get("fname")
        tf = str(filename) + ".mp3"
        path = os.getcwd()
        sf = tts.save(path + '/media/audio/'+tf)
#        sf = tts.save('/media/audio/'+tf)
        context = {
            "iw" : txt,
            "fname" : filename,
            "sf" : sf,
            "tf" : tf,
        }
    return render(request, "tts/index.html", context)

# 수정해야함!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 아래꺼 지워야함!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 질문하려고 남겨놓은거임!!!!!!!!!!!!!!!!!!!!!!
###
    if request.method == "POST":
        txt = request.POST.get("iw")
        tts = gTTS(text=txt, lang='ko')
        filename = request.POST.get("fname")
        tf = str(filename) + ".mp3"
        sf = tts.save(tf)
        context = {
            "iw" : txt,
            "fname" : filename,
            "sf" : sf,
            "tf" : tf,
        }
    return render(request, "tts/index.html", context)
###