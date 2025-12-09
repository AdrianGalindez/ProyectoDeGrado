# ==========================================IMPORTACIONES================================================
import ollama #importación de la librería ollama
from .llm import guardar_historial, llm, obtener_historial, verificar_tipo_de_usuario
from langchain_core.prompts import PromptTemplate #importación de la clase PromptTemplate desde langchain.templates

# ========================================================================================================

# ==========================================CHAINS=========================================================
template = PromptTemplate(   # creación de una plantilla de prompt
    input_variables=["nombre"], #definición de las variables de entrada para la plantilla
    template="saluda al usuario siempre en español y con emogis y dile que te llamas Adrian the Goat y siendo el mejor programador estas aqui para ayudarlo\n : {nombre} \n Asistente:" #definición de la plantilla con una pregunta
)

chain = template | llm  # creación de una cadena que combina la plantilla de prompt con el modelo LLM


# ===================================================================================================

def get_chain(nombre: str) :
    prompt = nombre
    guardar_historial(prompt)
    # historial = obtener_historial()
    # print("Historial guardado:", historial)
    # tipo_usuario=verificar_tipo_de_usuario(historial)
    # print("Tipo de usuario verificado:", tipo_usuario)
    return chain.invoke({"nombre" : nombre}) #, "chat_history": historial}).text


def get_historial_chain():
    historial = obtener_historial()
    print("Historial obtenido en views:", historial)
    return historial