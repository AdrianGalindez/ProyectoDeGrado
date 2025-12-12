# ==========================================IMPORTACIONES================================================
import ollama #importación de la librería ollama

from .llm import guardar_historial, llm, obtener_historial, verificar_tipo_de_usuario

from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder #importación de la clase PromptTemplate desde langchain.templates

from langchain_core.runnables import Runnable,RunnableLambda,RunnableParallel

import json
# ========================================================================================================

# ==========================================CHAINS=========================================================
template = PromptTemplate(   # creación de una plantilla de prompt
    input_variables=["nombre"], #definición de las variables de entrada para la plantilla
    template="saluda al usuario siempre en español y con emogis y dile que te llamas Adrian the Goat y siendo el mejor programador estas aqui para ayudarlo\n : {nombre} \n Asistente:" #definición de la plantilla con una pregunta
)

chain_saludo = template | llm  # creación de una cadena que combina la plantilla de prompt con el modelo LLM


# ===================================================================================================

def get_chain(nombre: str) :
    prompt = nombre
    guardar_historial(prompt)
    # historial = obtener_historial()
    # print("Historial guardado:", historial)
    # tipo_usuario=verificar_tipo_de_usuario(historial)
    # print("Tipo de usuario verificado:", tipo_usuario)
    return chain_saludo.invoke({"nombre" : nombre}) #, "chat_history": historial}).text


def get_historial_chain():
    historial = obtener_historial() or []
    return historial
# ========================================================================================

# =============================================RUNNEABLES ANALISIS DE SENTIMIENTOS RESEÑAS =========================================================

def procesar_textos(text): # funcion para limitar el texto hasta 500 caracteres
    if isinstance(text,dict):
        text = text.get("prompt") or text.get("texto") or text.get("nombre") or ""
    return str(text).strip()[:500]

procesador=RunnableLambda(procesar_textos)  # convierte la funcion procesar_textos a runneable 


def get_resumen(text):   # funcion para generar el resumen 
    prompt=f"genera un resumen de el siguiente texto en una sola frase no respondas nada solo haz un resumen texto : {text}"
    respuesta= llm.invoke(prompt)
    return respuesta


resumen_branch= RunnableLambda(get_resumen) # convierte la funcion get_resumen en un RUnnable


def analizar_sentimiento(text):  # funcion para nalizar el sentimiento
    prompt= f'''analiza el sentimiento del siguiente texto.responde unicamente en formato Json valido 
    {{"sentimiento": "bueno|malo|neutro",
      "razón": justificacion breve }} : {text}'''
    respuestas = llm.invoke(prompt)
    try:
        return json.loads(respuestas)
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "error de analisis" }
    

sentimiento_branch=RunnableLambda(analizar_sentimiento) # convierte la funcion analizar sentimiento en Runnable

def unir_resultados(data):      # funcion para unir "merge" resultados
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



def get_respuestas(reseñas):
   return chain.batch(reseñas)


# ===========================================================================================================


#===========================================RUNNEABLES GENERAR CUESTONARIOS==================================================================

def generar_cuestionarios(text):
    prompt = f'''genera un cuestionario tipo icfes en español.
    responde unicamente en formato Json valido sin texto adicional.
    no generes listas ni multiples objetos
    estructura obligatoria:
    {{"pregunta": "",
    "A": "",
    "B": "",
    "C": "",
    "D": ""}} tema: {text}'''
    respuesta= llm.invoke(prompt)
    # respuesta_jason=convertir_Json_Valido(respuesta)
    try:
        return json.loads(respuesta)
    except json.JSONDecodeError:
        return {
            "pregunta": "error al generar cuestionario",
            "A": "",
            "B": "",
            "C": "",
            "D": ""
        }
    

cuestionario_branch= RunnableLambda(generar_cuestionarios) # convertir la funcion generar cuestionario en Runneable

chain_cuestionarios= procesador | cuestionario_branch


def get_Cuestonarios(text):
     return chain_cuestionarios.invoke(text)

#=============================================================================================================================================


 #=========================================TEMPLATES=================================================

template = "eres un experto en educacin sugiere temas de estudio basandote en las siguientes falencias de educacion {falencias}"

prompt= PromptTemplate(
    template=template,
    input_variables=["falencias"]
)

llamada_prompt=prompt.format(falencias="matematicas")


chat_prompt= ChatPromptTemplate.from_messages([
    ("system", ''' eres un generador estricto de JSON.
    genera una unica pregunta tipo ICFES.
    el formato del cuestionario debe ser opcion multiple unica respuesta.
    responde unicamente en formato Json valido sin texto adicional.
    no generes listas ni multiples objetos.
    no repeitas preguntas.
    estructura obligatoria \n:
    {{"pregunta": "",
    "A": "",
    "B": "",
    "C": "",
    "D": "",
    "respuesta_correcta":""}}'''),
    ("human","{texto}")
])


def get_respuesta(mensages):
   respuesta= llm.invoke(mensages)
   try:
        return json.loads(respuesta)
   except json.JSONDecodeError:
        return {
            "pregunta": "error al generar cuestionario",
            "A": "",
            "B": "",
            "C": "",
            "D": "",
            "respuesta_correcta": ""
        }
  
 #===================================================================================================