import requests
import asyncio
import os
from groq import Groq
from bs4 import BeautifulSoup

# Obtener claves API desde variables de entorno
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SERPER_URL = "https://google.serper.dev/search"

# Inicializar cliente de Groq
client = Groq(api_key=GROQ_API_KEY)

# Función para hacer una búsqueda en Google usando Serper.dev
def buscar_en_google(consulta):
    """
Performs a Google search using the Serper.dev API and retrieves the top 5 organic search results.

Args:
    consulta (str): The search query to be sent to the API.

Returns:
    list: A list containing up to 5 organic search results. Returns an empty list if an error occurs.

Raises:
    requests.exceptions.RequestException: If there is an issue with the network request.
"""
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": consulta}
    
    try:
        response = requests.post(SERPER_URL, json=payload, headers=headers)
        response.raise_for_status()  # Para asegurarse de que no haya errores de red
        return response.json().get("organic", [])[:5]  # Tomar los primeros 5 resultados
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar en Google: {e}")
        return []

# Función para extraer el contenido de una página web
def extraer_texto(url):
    """
Extracts text content from a given URL.

This function sends a GET request to the specified URL and parses the HTML content
to extract text from all paragraph tags. The extracted text is limited to 1000 characters.
If an error occurs during the request or parsing, an error message is returned.

Args:
    url (str): The URL of the web page to extract text from.

Returns:
    str: The extracted text content or an error message if extraction fails.
"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Asegúrate de que la respuesta sea exitosa
        soup = BeautifulSoup(response.text, "html.parser")
        texto = " ".join([p.text for p in soup.find_all("p")])[:1000]  # Limitar a 1000 caracteres
        return texto
    except Exception as e:
        return f"Error al obtener contenido de {url}: {e}"

# Función para generar respuestas con Groq
async def generar_respuesta(consulta, contexto):
    """
    Generates a response to a user query using the Groq language model.
    
    This asynchronous function constructs a conversation context by appending the
    user's query to the existing context and requests a completion from the Groq
    language model. The response is generated in a streaming manner, simulating
    real-time interaction by printing each chunk of the response as it is received.
    The final response is returned as a concatenated string.

    Args:
        consulta (str): The user's query to be processed.
        contexto (list): The existing conversation context, consisting of a list
            of message dictionaries.

    Returns:
        str: The generated response from the language model.
    """
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=contexto + [{"role": "user", "content": consulta}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    respuesta = ""
    for chunk in completion:
        respuesta += chunk.choices[0].delta.content or ""
        await asyncio.sleep(0.05)  # Simulación de streaming
    
    return respuesta


# Bucle principal del chatbot
async def main():
    """
    Runs the main loop for the chatbot application.
    
    This asynchronous function initializes the conversation context and continuously
    prompts the user for input until 'salir' is entered. It performs a Google search
    for each user query, extracts relevant text from the search results, and uses
    the Groq language model to generate a response. The conversation context is
    updated with each interaction to improve response relevance. The function also
    displays the sources of the extracted information.

    Returns:
        None
    """
    print("Bienvenido al chatbot. Escribe 'salir' para terminar.")
    contexto = []  # Memoria de conversación
    
    while True:
        consulta = input("> Usuario: ")
        if consulta.lower() == "salir":
            break
        
        print("\n> Chatbot: ** Buscando en internet... **")
        resultados = buscar_en_google(consulta)
        
        fuentes = []
        contenido_relevante = ""
        
        for res in resultados:
            url = res.get("link", "")
            if url:
                fuentes.append(url)
                contenido = extraer_texto(url)
                contenido_relevante += contenido + "\n"
                #print(f"Fuente encontrada: {url}")
        
        # Asegúrate de que el contexto se actualice con el contenido relevante extraído
        contexto.append({"role": "assistant", "content": contenido_relevante})
        print("\n> Chatbot: ** Generando respuesta... **")
        
        contexto.append({"role": "user", "content": consulta})

        # Genera la respuesta completa
        respuesta = await generar_respuesta(consulta, contexto)
        
        contexto.append({"role": "assistant", "content": respuesta})

        # Imprimir solo una vez la respuesta completa
        print("\n> Chatbot: " + respuesta)
        
        # Mostrar las fuentes de donde se extrajo la información
        print("\nReferencias:")
        for fuente in fuentes:
            print(f"- {fuente}")

        
# Ejecutar el chatbot
if __name__ == "__main__":
    asyncio.run(main())
