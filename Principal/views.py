from django.shortcuts import render

# Create your views here.       

def home(request):
    #                                ,{"clave":valor}
   return render(request,"home.html" )       # view home

