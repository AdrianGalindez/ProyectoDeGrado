from django.shortcuts import render

# Create your views here.       

def home(request):
    #                                ,{"clave":valor}
   return render(request,"home.html" )       # view home

def test(request):
    return render(request,"TestDeVocacion.html")     # view test de vocacion 

def recomendaciones(request):
    return render(request,"Recomendaciones.html")     # view recomendacion de carreras con IA

def carreras(request):
    return render(request,"Carreras.html")     # view Carreras Profesionales

def comparadorDeCarreras(request):
    return render(request,"ComparadorDeCarreras.html")     # view Comparador de carreras 

def configuraciones(request):
    return render(request,"Configuraciones.html")     # view Cnfiguraciones

def perfil(request):
    return render(request,"PerfilDeUsuario.html")     # view Perfil de usuario

def inicioDeSesion(request):
    return render(request,"InicioSesion.html")     # view iniciar secion 

def registro(request):
    return render(request,"Registro.html")     # view Registrarse