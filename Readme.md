# Chatbot con Integración de Búsqueda Web

Este es un chatbot que utiliza **Serper.dev** para realizar búsquedas en Google y **Groq** para generar respuestas inteligentes basadas en el contexto obtenido de los resultados de búsqueda. El chatbot extrae contenido relevante de las páginas web encontradas y lo utiliza para construir respuestas precisas.

## Descripción

El chatbot responde a las consultas del usuario buscando información en línea, extrayendo el texto relevante de las páginas web encontradas y generando una respuesta utilizando el modelo de lenguaje **Groq**. También proporciona las fuentes de donde se extrajo la información para mayor transparencia.

## Funcionalidad

1. **Búsqueda en Google**: Utiliza la API de **Serper.dev** para buscar en Google y obtener los primeros 5 resultados relevantes.
2. **Extracción de contenido web**: Extrae el contenido de las páginas web encontradas utilizando **BeautifulSoup** para procesar el HTML.
3. **Generación de respuestas**: Utiliza el modelo de lenguaje **Groq** para generar respuestas basadas en el contenido relevante extraído.
4. **Memoria de conversación**: Mantiene un contexto de la conversación para que las respuestas se ajusten a la interacción previa.
5. **Referencias**: Al final de cada respuesta, se muestran las fuentes de donde se extrajo la información.

## Dependencias

Este proyecto requiere las siguientes librerías de Python:

- `requests`: Para realizar peticiones HTTP a las APIs y páginas web.
- `asyncio`: Para manejar la programación asíncrona en la generación de respuestas.
- `os`: Para manejar variables de entorno.
- `groq`: Cliente para interactuar con la API de **Groq**.
- `beautifulsoup4`: Para procesar el contenido HTML de las páginas web.

### Instalación de dependencias

Puedes instalar las dependencias con `pip` usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Configuración

Variables de entorno

Para que el chatbot funcione correctamente, es necesario configurar las claves de API para Serper.dev y Groq como variables de entorno. Asegúrate de tener las claves API y configurarlas de la siguiente manera:

    SERPER_API_KEY: Clave API de Serper.dev para realizar búsquedas en Google.
    GROQ_API_KEY: Clave API de Groq para generar respuestas inteligentes.

```
Ejemplo de configuración de variables de entorno:

export SERPER_API_KEY="tu_clave_serper"
export GROQ_API_KEY="tu_clave_groq"
```


Uso

Para ejecutar el chatbot, simplemente ejecuta el archivo Python principal:

```bash
    python chatbot.py
```
Una vez ejecutado, el chatbot te pedirá que ingreses una consulta. El chatbot buscará información en la web, extraerá contenido relevante de las páginas y generará una respuesta basada en esa información. También mostrará las fuentes utilizadas.

Comandos

    salir: Termina la ejecución del chatbot.

Ejemplo de uso


Bienvenido al chatbot. Escribe 'salir' para terminar.
> Usuario: ¿Qué es la inteligencia artificial?
> Chatbot: ** Buscando en internet... **
Fuente encontrada: https://example.com/ai
...
> Chatbot: La inteligencia artificial (IA) se refiere a la simulación de procesos de inteligencia humana mediante algoritmos y sistemas computacionales...
Referencias:
- https://example.com/ai


