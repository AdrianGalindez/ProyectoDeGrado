# ================================IMPORTACIONES===============================================
from itertools import chain
from django.shortcuts import render
from django.http import JsonResponse #, HttpResponse
from .IA.chains import get_chain, get_historial_chain
# ===============================================================================

# Create your views here.       


# =================================HOME=======================================
def home(request):
    if request.method=="POST":
        nombre=request.POST.get("prompt","")
    else:
        nombre = "haru"
    respuesta = get_chain(nombre)
    historial=get_historial_chain()
    if request.method == "POST" and "borrarHistorial" in request.POST:
        historial.clear()  # Clear the history list
    return render(request,"home.html",{"respuesta": respuesta, "historial": historial})       # view home
# ==============================================================================



# ==============================TEST===============================================
def test(request):
    if request.method=="POST":
        nombre=request.POST.get("prompt","")
    else:
        nombre = "haru"
    respuesta = get_chain(nombre)
    historial=get_historial_chain()
    return render(request,"TestDeVocacion.html", {"respuesta": respuesta, "historial": historial})     # view test de vocacion 
# ==============================================================================



# =============================RECOMENDACIONES======================================
def recomendaciones(request):
    return render(request,"Recomendaciones.html")     # view recomendacion de carreras con IA
# ============================================================================



# =============================CARRERAS======================================
def carreras(request):
    return render(request,"Carreras.html")     # view Carreras Profesionales
# ===========================================================================



# =============================COMPARADOR DE CARRERAS======================================
def comparadorDeCarreras(request):
    return render(request,"ComparadorDeCarreras.html")     # view Comparador de carreras 
# ===========================================================================



# =============================CONFIGURACIONES======================================
def configuraciones(request):
    return render(request,"Configuraciones.html")     # view Cnfiguraciones
# ====================================================================================



# =============================PERFIL DE USUARIO======================================
def perfil(request):
    return render(request,"PerfilDeUsuario.html")     # view Perfil de usuario
# ====================================================================================



# =============================INICIO DE SESION======================================
def inicioDeSesion(request):
    return render(request,"InicioSesion.html")     # view iniciar secion 
# ====================================================================================



# =============================REGISTRO ======================================
def registro(request):
    return render(request,"Registro.html")     # view Registrarse
# ===================================================================================



