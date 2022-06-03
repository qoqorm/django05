from django.urls import path
from . import views

app_name = "trans"

urlpatterns = [
    path('index3/', views.index3, name='index3'),
    path('index2/', views.index2, name='index2'),
    path('index/', views.index, name='index'),
#    path('detail/<bpk>', views.detail, name='detail'),
#    path('create/', views.create, name='create'),
#    path('logout/', views.userlogout, name='logout'),
#    path('profile/', views.profile, name='profile'),
#    path('delete/<bpk>', views.delete, name='delete'),
#    path('update/<bpk>', views.update, name='update'),
]