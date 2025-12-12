# ================================IMPORTACIONES===============================================
from itertools import chain
from django.shortcuts import render
from django.http import JsonResponse #, HttpResponse
from .IA.chains import get_chain, get_historial_chain,get_respuestas,get_Cuestonarios,chat_prompt,get_respuesta
# ===============================================================================

# Create your views here.       


# =================================HOME=======================================
def home(request):
    if request.method=="POST":
        nombre=request.POST.get("prompt","")
    else:
        nombre = "haru"
    frase = get_chain(nombre)
    historial=get_historial_chain() or []
    reseñas = ["este curso me ha gustado es muy bueno",  # conjunto de reseñas
           "mas o menos el curso es normal pero no tiene nada epecial",
           "no me ha gustado nada muy malo y muy basico"
           ]
    resumen= get_respuestas(reseñas)
    if request.method == "POST" and "borrarHistorial" in request.POST:
        historial.clear()  # Clear the history list   
    return render(request,"home.html",{"frase": frase, "historial": historial,"resumen": resumen[0]["resumen"]})       # view home
# ==============================================================================



# ==============================TEST===============================================
def test(request):
    if request.method=="POST":
        nombre=request.POST.get("prompt","")
    else:
        nombre = "haru"
    frase = get_chain(nombre)
    historial = get_historial_chain() or []
    if request.method=="POST":
        materia=request.POST.get("materia","")
    else:
        materia = "Ingles"
    mensages=chat_prompt.format_messages(
         texto =materia
    )
    quizes = []
    for i in range(9):
       mensages= chat_prompt.format_messages(texto=materia)
       quiz=get_respuesta(mensages)
       quiz["id"]=i
       quizes.append(quiz)
    print(quizes)
    contexto= range(1,10)
    return render(request,"TestDeVocacion.html", {"frase": frase, "historial": historial,"quizes": quizes,"contexto": contexto})     # view test de vocacion 
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



