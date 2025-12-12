# ==========================================IMPORTACIONES================================================
import ollama #importación de la librería ollama

from langchain_community.llms import Ollama #importación de la clase Ollama desde langchain_community

from langchain_core.prompts import PromptTemplate #importación de la clase PromptTemplate desde langchain.templates

from langchain_core.messages import AIMessage,HumanMessage, SystemMessage #importación de la clase PromptTemplate desde langchain.templates

from django.core.cache import cache  #importación de la clase cache desde django.core.cache

# from langchain_core.runnables import Runnable,RunnableLambda,RunnableParallel

# import json
# ==========================================================================================


llm = Ollama(model="llama3",temperature=0.7) #creación de una instancia del modelo LLM con el modelo "llama3" y una temperatura de 0.7 una temperatura baja es menos creativo una temperatura alta es mas creativo



 

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
