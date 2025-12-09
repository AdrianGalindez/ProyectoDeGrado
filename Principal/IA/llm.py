# ==========================================IMPORTACIONES================================================
import ollama #importación de la librería ollama

from langchain_community.llms import Ollama #importación de la clase Ollama desde langchain_community

from langchain_core.prompts import PromptTemplate #importación de la clase PromptTemplate desde langchain.templates

from langchain_core.messages import AIMessage,HumanMessage, SystemMessage #importación de la clase PromptTemplate desde langchain.templates

from django.core.cache import cache  #importación de la clase cache desde django.core.cache

from langchain_core.runnables import Runnable,RunnableLambda,RunnableParallel

import json
# ==========================================================================================


llm = Ollama(model="llama3",temperature=0.2) #creación de una instancia del modelo LLM con el modelo "llama3" y una temperatura de 0.7 una temperatura baja es menos creativo una temperatura alta es mas creativo



# =============================================RUNNEABLES=========================================================

def procesar_textos(text): # funcion para limitar el texto hasta 500 caracteres
    return text.strip()[:500]

procesador=RunnableLambda(procesar_textos)  # convierte la funcion procesar_textos a runneable 


def get_resumen(text):   # funcion para generar el resumen 
    prompt=f"genera un resumen de el siguiente texto en una sola frase no respondas nada solo haz un resumen texto : {text}"
    respuesta= llm.invoke(prompt)
    return respuesta

resumen_branch= RunnableLambda(get_resumen) # convierte la funcion get_resumen en un RUnnable


def analizar_sentimiento(text):  # funcion para nalizar el sentimiento
    prompt= f'analiza el sentimiento del siguiente texto.responde unicamente en formato Json valido {{"sentimiento": "bueno|malo|neutro" "razón": justificacion breve }} : {text}'
    respuestas = llm.invoke(prompt)
    print("-----------------------------------------------")
    print("esta es la respuesta : \n"+respuestas)
    print("-----------------------------------------------")
    try:
        return json.loads(respuestas)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "error de analisis" }
    

sentimiento_branch=RunnableLambda(analizar_sentimiento) # convierte la funcion analizar sentimiento en Runnable

def unir_resultados(data):      # funcion para unir "merge" resultados
    # print(data["sentimiento_data"])
    return {"resumen": data["resumen"],
            "sentimiento": data["sentimiento_data"]["sentimiento"],
            "razon": data["sentimiento_data"].get("razón") or  data["sentimiento_data"].get("razon")
            }


def convertir_Json_Valido(texto):
    json_valido=json.dumps(texto,ensure_ascii=False,indent=2) # convertir Json a json valido
    return json_valido


unir = RunnableLambda(unir_resultados)  # convierte la funcion unir resultado en Runnable 
    
analisis_paralelo = RunnableParallel({
    "resumen": resumen_branch,
    "sentimiento_data": sentimiento_branch
})


# cadena "chain" completa 

chain= procesador | analisis_paralelo | unir

reseñas = ["este curso me ha gustado es muy bueno",  # conjunto de reseñas
           "mas o menos el curso es normal pero no tiene nada epecial",
           "no me ha gustado nada muy malo y muy basico"
           ]

respuestas = chain.batch(reseñas) # ejecutar varias cadenas al mismo tiempo 

print(respuestas)
json_valido= convertir_Json_Valido(respuestas)# convertir Json a json valido
print("-------------------------------------esto es json valido------------------------------ : \n"+json_valido)

# chain1=RunnableLambda(lambda x: f"numero {x}")

# def duplicarTexto(text):
#     return [text] * 2

# chain2 = RunnableLambda(duplicarTexto)

# chains= chain1 | chain2

# resultado = chains.invoke(43)

# print(resultado)
# ===========================================================================================================


 

# ============================================HISTORIAL DE MENSAGES============================================================

def guardar_historial(prompt: str):    
    historial = cache.get("chat_history") or []  #obtención del historial de mensajes almacenados en la caché
    mensaje = HumanMessage(content=prompt)  #creación de un mensaje 
    historial.append(mensaje)  #adición del mensaje al historial
    cache.set("chat_history", historial)  #almacenamiento del historial actualizado en la caché



def guardar_respuesta_ai(respuesta_ai):
    historial = cache.get("chat_history") or []  #obtención del historial de mensajes almacenados en la caché
    mensaje = AIMessage(content=respuesta_ai)  #creación de un mensaje 
    historial.append(mensaje)  #adición del mensaje al historial
    cache.set("chat_history", historial)  #almacenamiento del historial actualizado en la caché
    return historial



def obtener_historial():    
    historial = cache.get("chat_history") #obtención del historial de mensajes almacenados en la caché
    return historial



def eliminar_historial():
    cache.delete("chat_history")  #eliminación del historial de mensajes almacenados en la caché


def verificar_tipo_de_usuario(historial):
  historial = cache.get("chat_history") or []  #obtención del historial de mensajes almacenados en la caché
  for message in historial:  #iteración sobre los mensajes almacenados en el historial de la caché
    if isinstance(message, HumanMessage):  #verificación si el mensaje es del tipo HumanMessage
        print(f"Usuario: {message.content}")  #impresión del contenido del mensaje del usuario
        rol = "usuario"
        print("====================ROL=================== \n" + rol)
    elif isinstance(message, AIMessage):  #verificación si el mensaje es del tipo AIMessage
        print(f"Asistente: {message.content}")  #impresión del contenido del mensaje del asistente
        rol = "asistente"
        print("====================ROL=================== \n" + rol)
    elif isinstance(message, SystemMessage):  #verificación si el mensaje es del tipo SystemMessage
        print(f"Sistema: {message.content}")  #impresión del contenido del mensaje del sistema
        rol = "sistema"
        print("====================ROL=================== \n" + rol)
    

# =========================================================================================================================
