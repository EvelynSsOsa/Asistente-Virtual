## esta libreria nos ayuda al reconocimiento de voz
import speech_recognition as sr ### convierte el audio del microfono a texto

#── funcionalidades del asistente ───────────────────────
import pywhatkit      ## nos ayuda a buscar un video en youtube y reproducirlo
import yfinance as yf ## nos ayuda a consultar el precio de las acciones en tiempo real
import pyjokes        ## nos ayuda a generar chistes o bromas
import webbrowser     ## nos ayuda a buscar URLs predeterminadas en el navegador
import datetime       ##nos con obtener la feche y la hora
import wikipedia      ## esta libreria nos ayuda a abstraer información de wikipedia
import time           ## nos ayuda a manejar las pausas del programa, ya sea para escuchar o para ejecutar alguna acción
import pyautogui      ## con este podemos simular teclas (pausa, play, siguiente video, tomar capturas etc...)
import subprocess     ## ejecuta comandos del sistema (applicaciones o control del volumen de las bocinas)

# ── traducción y búsqueda web ────────────────────────────
from deep_translator import GoogleTranslator   ## traduce texto de inglés a español import requests

# ── widget del asistente visual ──────────────────────────
from widget_nutria import NutriaWidget         ## aqui estamos importando nuestro archivo que contiene a los personajes flotantes
import threading                               ## permite correr tkinter y el asistente al mismo tiempo
import requests                                ##hace peticiones HTTP para buscar en internet
from bs4 import BeautifulSoup                  ## este nos ayuda a extraer texto de paginas web (el conocido 'web scraping')

# ── variables de entorno e IA ────────────────────────────
from dotenv import load_dotenv      ## carga variables del archivo .env de forma segura
import os                           ## accede a variables del sistema operativo
from google import genai            ## API de Gemini para respuestas de inteligencia artificial

# ── configuración de la IA ───────────────────────────────
load_dotenv()                        # carga el archivo .env, (que es el archivo, que contiene la contraseña el API key)
cliente_ia = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))    # conecta con Gemini

# ── personaje activo del asistente ───────────────────────
## estas variables nos vana a permitir identificar cual es el asistente activo
nutria = None ## petunia
jarifa = None ## Ramona
pato = None   ## Rigoberto


### escuchar nuestro microfono y devolver el audio como texto
def tranformar_audio_a_texto(silencioso=False):
    """
        Escucha el micrófono y convierte el audio capturado a texto.

        Parámetros:
            silencioso (bool): Si es True, suprime los mensajes de error y
                               la animación del widget. Se usa cuando hay un
                               video reproduciéndose para evitar captar su audio.

        Retorna:
            str: El texto reconocido, o "sigo esperando" si hubo algún error.
        """
    # almacenar el reconocedor en una variable
    r = sr.Recognizer()

    # configuracion del microfono, abre el microfono como fuente de audio
    with sr.Microphone() as origen:

        #tiempo de espera, que consideramos adecuado para saber que el usuario ya termino de hacer su petición
        r.pause_threshold = 0.8

        ## como el usuario esta hablando por lo tanto no estamos en silecio
        if not silencioso:
            # informar que comenzo la grabación, por medio de este print en consola
            print("Ya puedes hablar :)")
            if nutria:  # ← nutria muestra que está escuchando
                nutria.mostrar_escuchando() ## madamos a llamar a la función del widget, donde podemos ver a la Petunia o cualquier
                ## otro asistente con su boquita abierta y en la burbuja de abajo dice "Escuchando"

        #en esta variable guardamos el audio capturado por el microfono
        audio = r.listen(origen)

        try:
            ## envía el audio a Google para convertirlo a texto en español mexicano
            pedido = r.recognize_google(audio, language="es-mx")

            #prueba de que puedo ingresar y tranformar nuestra voz en un texto que se puede imprimir
            print("Dijiste: " + pedido) ## este basicamente nos ayuda, para ver que fue lo que se detecto
            ## en la petición

            # devolver pedido, ya en español
            return pedido

        # en caso de Google no haya podido interpretar nuestras palabra, quiere decir que no podra realizar el pedido
        except sr.UnknownValueError:
            if not silencioso:
                # prueba de que no comprendio el audio
                hablar("rayos creo que no entendí lo que dijiste")
            #devolver error
            return "sigo esperando"

        # en caso de no poder resolver el pedidio, no se pudo conectar al servicio de Google, (no hay internet)
        except sr.RequestError:
            if not silencioso:
                # prueba de que no comprendio el audio
                hablar("rayos no hay servicio")
            # devolver error
            return "sigo esperando"

        ## error ineperado
        except:
            if not silencioso:
                # prueba de que no comprendio el audio
                hablar("rayos, algo salio mal")

            # devolver error
            return "sigo esperando"


def bajar_volumen_navegador():
    """
        Baja el volumen del sistema al 15% usando AppleScript.
        Se llama justo después de que el asistente habla, para que
        el video de fondo no tape la voz del usuario ni del asistente.
        Solo funciona en Mac.
        """
    subprocess.run(['osascript', '-e','set volume output volume 15'])

def subir_volumen_navegador():
    """
        Restaura el volumen del sistema al 80% usando AppleScript.
        Se llama justo después de que el asistente termina de hablar,
        para que el video de fondo vuelva a escucharse con normalidad.
        Solo funciona en Mac.
        """
    subprocess.run(['osascript', '-e', 'set volume output volume 80'])


 ## función para que el asistente pueda ser escuchado


def hablar(mensaje):
    global nutria
    if nutria:
        """ 
        root:
            En la clase de "NutriaWidget" tenemos un atributo de clase, que se llama "root" y basicmanete es el que 
            nos ayuda a poder visualizar una ventana con la animación de nuestro asistente 
        after : 
            Es un metodo de tkinter que significa "ejecuta esto(root) en el hilo principal de tkinter" 
             El 0 significa "ejecutalo lo antes posible"
        lambda: 
            nos ayuda a empaquetar el mensaje y poder pasarlo como argumento a la función "iniciar_hablar"
            el argumento se guardo en la variable "m" - > "nutria.root.after(0, lambda m=mensaje: nutria.iniciar_habla(m))"
        """
        nutria.root.after(0, lambda m=mensaje: nutria.iniciar_habla(m))

    """nutria.personaje contiene el personaje activo guardado en
    "self.personaje = personaje" dentro de la función "actualizar_personaje()" de "widget_nutria"
    dependiendo de su valor, se asigna la voz correspondiente"""
    if nutria.personaje == 'nutria':
        voz = 'Monica' ## le asignamos la voz de Monica
    elif nutria.personaje == 'pato': ## si decimos que el personaje sera iguala a pato
        voz = 'Grandpa (Español (México))' ## decimos que su voz sera esta de aquí
    elif nutria.personaje == 'jarifa':
        voz = 'Flo (Español (México))'
    else:
        voz = 'Monica'

    # sintetiza la voz usando el comando say de Mac
    # -v → nombre de la voz a usar
    # -r → velocidad en palabras por minuto (150 = velocidad normal)
    subprocess.run(['say', '-v', voz, '-r', '150', mensaje])

    # una vez que termina de hablar, detiene la animación de boca (NOTA SUPER IMPORTANTE)
    if nutria: ## importante recordar que el 0 nos indica que "se ejecuta lo antes posible""
        nutria.root.after(0, nutria.parar_habla) ## y madamos a llamamr a la anaimcaión donde el personaje deja de hablar
        ## por medio de la función "parar_hablar"
    ## esta función la podemos ver en el archivo "widget_nutria.py", su flujo es el siguiente
    #Flujo:
        #1. Cambia la bandera 'hablando' a False para detener _animar()
        #2. Cancela el after() pendiente de tkinter si existe
        #3. Regresa al personaje a su estado idle (boca cerrada)#



## esta función nos ayuda a sacar el día de la semana
def pedir_dia():
    #craer variable con el metodo de "datetime"
    # y de ahí podemos sacar la fehca ".date" y el día ".today()"
    dia = datetime.date.today()

    # crear variable que nos va a guardar, una instancia de la variable "dia" linea 181 y con
    ## "weekday()" sacamos el día de la semana (literalmente el número de la semana)
    dia_semana= dia.weekday()
    print(dia_semana) ## con esto podemos saber que número de la semana tenemos el día de hoy

    ## diccionario con nombres de los dias, cada uno de estos días corresponde a un nombre
    calendario = {0:'Lunes', ## el 0 le correponde al lunes y así sucesivamente
                  1:'Martes',
                  2:'Miércoles',
                  3:'Jueves',
                  4:'Viernes',
                  5:'Sábado',
                  6:'Domingo' ## hasta llegar al día numero 6 con el Domingo
                  }

    ## decir el dia de la semana, y para ello mandamos a llamar al método "hablar" y le pasamos
    ## como parametro el calendario  y entre corchetes pasamos el dia de la semana que queremos con la variable
    ## "dia_semana"
    hablar(f'Hoy es {calendario[dia_semana]}')


## informar hora
def pedir_hora():
    ## crear una variable, donde madamos a llamar al metodo "datetime" junto con ".now()" que nos ayuda a saber la hora exacta
    hora = datetime.datetime.now()
    ## entonces decimos que la variable "hora" sera una cadena de texto
    ## donde decimos que nos traiga la hora -> "hora.hour"
    ## donde decimos que nos traiga los minutos -> "hora.minute"
    ## y que nos traiga los segundos -> "hora.second"
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora) ## ahora imprimimos en pantalla "hora"
    # decir la hora
    hablar(hora) ## aqui estamos mandando a llamar a la función mientras le pasamos el parametro de hora
    ## con eso el asistente nos podra decir la hora exacta, con minutos y segundos incluidos

# fucnión para el saludo inicial
def saludito():
    ## crear variable que nos indicara la hora, esto nos va ayudar a saber si es de tarde, de noche o de día
    hora = datetime.datetime.now()
    # si todavia no son las 6 de la mañana, pero si soy más de las 8 de la noche
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'##damos las buenas noches
    elif 6 <= hora.hour < 13: ## si hora es mayor a las 6 de la mañana y menor a la una de la tarde
        momento = 'Buen día' ## dmos los buenos días
    else: ## por descarte las buens tardes, else seran las buenas tardes ,es decir de un horario de la una a las 7 de la noche
        momento = 'Buenas tardes'
## dependiendo en donde haya caido la condición del momento, decimos buenas tardes, buenas noches o buenos días
    ## junto con la presentación deL asistente, que por Default sera Petunia la Nutria
    hablar(f'{momento}, soy Petunia tú asistente personal, Por favor dime en que te puedo ayudar')

######################  EXPLICACIÓN DE LA FUNCIÓN "modalida_video()"
"""
        Pone al asistente en modo silencio cuando se reproduce un video.
        Se manda llamar cada vez que algo empieza a sonar.

        La animación de boca se maneja automáticamente dentro de hablar(),
        por lo que no es necesario activarla aquí directamente.
        (esto lo podemos ver en la función hablar() en la línea 165)

        Flujo:
            1. El asistente dice su nombre para que el usuario sepa
               cómo llamarlo cuando lo necesite
            2. Sube el volumen del sistema al terminar de hablar
            3. Devuelve True para activar la bandera 'reproduciendo'
               en el while de pedir_cosas()

        Conexión con pedir_cosas():
            La función por sí sola no sabe nada del while, solo devuelve True.
            Es pedir_cosas() quien recibe ese True y activa la bandera:

            reproduciendo = modalidad_video()  ← recibe True
                ↓
            while detecta reproduciendo = True
                ↓
            if reproduciendo:
                pedido = tranformar_audio_a_texto(silencioso=True)
                # el micrófono solo escucha el nombre del asistente activo
                # ignora cualquier otro sonido (incluyendo el audio del video)

        Retorna:
            bool: True para indicar que hay un video reproduciéndose
                  y activar el modo silencio en el while de pedir_cosas()
        """
#####################
def modalidad_video ():
    global nutria
    # avisa al usuario cómo llamar al asistente activo
    if nutria.personaje == 'nutria':
        hablar('Di Petunia cuando me necesites')
    elif nutria.personaje =='pato':
        hablar('Di Rigoberto, si me necesitas')
    elif nutria.personaje == 'jarifa':
        hablar('Di Ramona, si necesitas algo ')

    subir_volumen_navegador() # restaura el volumen del sistema después de hablar

    return True  # reproduciendo = True en la función de pedir cosas, activamos la bandera

#######################
"""
    Traduce cualquier texto al español usando Google Translator.
    Se usa principalmente cuando Wikipedia no encuentra información
    en español y tiene que buscar en inglés.

    Parámetros:
        texto (str): El texto a traducir, puede estar en cualquier idioma.
                     source='auto' detecta el idioma automáticamente.

    Retorna:
        str: El texto traducido al español, o el texto original
             si la traducción falla.
    """
#######################
def traducir_a_espanol(texto): ## creamos la función, junto con un parametro
    try:## entonces este bloque tratará de ejecutar, la siguiente instrución
        return GoogleTranslator(source='auto', target='es').translate(texto)
        ## GoogleTranslator pertenece a la librería deep-translator
        ## source='auto' indica que el idioma de origen se detectará automáticamente
        ## target='es' indica que el resultado debe traducirse en español
        ## madamos a llamar al metodo "translate" y le pasamos como parametro el texto que tenemos como parametro
    except: ## en dado caso de no haber podido traducir ningun texto
        return texto ## regresamos el texto tal cual lo encontramos

#######################
"""
    Busca un término en Google y extrae el primer resultado encontrado.
    Se manda llamar desde la condición 'busca en internet' en pedir_cosas().

    Flujo:
        1. Construye la URL de búsqueda de Google con el término
        2. Hace una petición HTTP simulando ser un navegador real
           (User-Agent evita que Google bloquee la petición)
        3. Extrae el snippet del primer resultado con BeautifulSoup
        4. Traduce el resultado al español si está en otro idioma

    Parámetros:
        termino (str): El texto a buscar en Google.

    Retorna:
        str: El texto del primer resultado traducido al español,
             o None si no encontró nada o hubo un error.
    """
#######################
def buscar_y_leer(termino):
    try:## vamos a ejecutar el siguiente bloque:
        headers = {'User-Agent': 'Mozilla/5.0'}## creamos un diccionario,
        # la llave "User-Agent" le indica al servidor quien esta realizando la petición, esto con la intención de que
        ## google no detecte que se está haciendo una busqueda, por medio de un programa, es decir que nos estamos
        # haciendo pasar por un navegador
        url = f'https://www.google.com/search?q={termino}'## construimos la liga y le pasamos nuestro parametro, con esto lo que logramos es
        ## crear la liga, para hacer la busqueda de lo que queramos
        res = requests.get(url, headers=headers) ## ahora realizamos la petición http get, como parametros tenemos a
        # "url", que es la dirección que contruimos en la linea anterior
        ## "headers" que son la llave que nos va ayuadar a hacernos pasar por un navegador web
        soup = BeautifulSoup(res.text, 'html.parser') ## esta linea nos va ayudar a analizar bien el http
        ## sabemos que "BeautifulSoup" es una libreria que nos ayuda a analizar los html
        ## en "res.text" -> tenemos lo que contiene esta busqueda, (como el archivo html)
        ## y con "html.parser" -> tenemos al analizador que vamos a usar, para interpretar el codigo/ archvio html
        snippet = soup.find('div', class_='BNeawe')
        ## en la variable "snippet", vamos a utilizar el metodo "soup.find" a la que le vamos a pasar como parametro
        ##"div" es decir una etiqueta de este tipo
        ##"class_='BNeawe'" -> indicamos que la etiqueta debe de tener la clase "BNeawe"...
        ## que es la clase que utiliza google para visualizar ciertos fragmentos
        if snippet: ## en dado caso de que si hayamos podido obtener el snippet, es decir el fragmento
            return traducir_a_espanol(snippet.get_text())## vamos a mandar a llamar a la función "traducir_a _español"
        ## y le vamos a pasar como parametro "snippet.get_text()" que nos va ayudar a extraer el texto que haya encontrado en esa etiqueta
        return None
    except: ## y en dado caso de no haber encontrado ningun fragmento/ snippet
        return None ## no va a devolver nada

##############################################Explicación de la función "pregunta_a_ia":
"""
    Manda una pregunta a la API de Gemini y devuelve la respuesta.
    Se manda llamar desde la condición 'pregunta/oye ia' en pedir_cosas().

    El prompt le indica a Gemini que responda:
        - En español
        - De forma corta y clara
        - Máximo 3 oraciones

    Parámetros:
        pregunta (str): La pregunta que el usuario quiere hacerle a la IA.

    Retorna:
        str: La respuesta de Gemini en español,
             o None si hubo algún error con la API.
    """
##############################################
def preguntar_a_ia(pregunta):
    try:## vamos a intenatar ejecutar el siguiente bloque:
      ## el metodo "generate_content(" nos ayuda a envíar una solicitud al modelo y genera una respuesta basada en el pront
        respuesta = cliente_ia.models.generate_content(
            model='gemini-flash-lite-latest', ## aquí decimos que modelo queremos utilizar
            contents=f'Responde en español de forma corta y clara, máximo 3 oraciones: {pregunta}'
            ## aquí estamos construyendo el pront, y pasamos como parametro la pregunta
        )
        return respuesta.text ## en dado caso de que este bloque haya sido ejecutado de forma correcta, entonces
    ## devolvera la repsuesta que obtuvimos, pero solo obtendrá el texto
    except Exception as e: ## decimos que si no se pudo ejecutar el bloque anterior
        print(f'Error IA: {e}') ## imprimimos en consola el error
        return None ## y no devolvemos nada



  # funcion central del asistente

def pedir_cosas():
    ## activar al saludo inicial, esto lo hacemos mandando a llamar a la función "saludito"
    saludito()

    #variable de corte -> comenzar nos ayuda a poder comenzar con el bucle
    comenzar = True
    ## luego tenemos a la variable "reproduciendo", la inicializamos en "False", porque aun no se esta reproduciendo
    ##ningún video
    reproduciendo = False
    ## loop central

    while comenzar: ## decimos que si comenzar en "True", estamos listos para poder escuchar cualquie petición del usuario
        ## si reproduciendo es "True", entonces:
        if reproduciendo:
            # activar el pedido, podemos ver que estamos en silencio porque el video se esta reproduciendo
            pedido = tranformar_audio_a_texto(silencioso=True).lower()
            ## en dado caso de escuhar un "Petunia", "Rigoberto" o "Ramona" en el pedido
            if 'petunia' in pedido or 'rigoberto' in pedido or 'ramona' in pedido:
                subir_volumen_navegador() ## madamos a llamar a la función para poder subir el volumen
                reproduciendo = False ## reproduciendo queda en False, para poder escuhar al usuario con su petición
                hablar('Dime, aquí estoy') ## entonces mandamos a llamar a la función "hablar" y le pasamos como parametro
                ##"Dime aquí estoy", la voz será del asistente activo en ese momento
            continue

        ## volvemos a activar el pedido... entonces mandamos a llamar a la función "tranformar_audio_a_texto()"
        pedido = tranformar_audio_a_texto().lower()
        print(f"Procesando: '{pedido}'") ### aquí estamos impirmiendo lo que creemos que es el pedido

        ## aqui caen todas nuestras condicionales que podemos encontrar en el pedido
        ##estas condicionales son palabras clave, que podemos encontar en el pedido, y dependiendo la palabra clave enontrada
        ## es lo que vamos a ejecutar

        if 'youtube' in pedido: ## si en pedido encontramos la palabra clave "youtube"
            ## madamos a llamar a la función hablar y con la voz del asistente activo, podremos escuchar el siguiente mensaje
            hablar('Con gusto estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')#solo abrirá youtube, pero con esta condición, no vamos a ejecutar ningún video
        elif 'navegador' in pedido:## si en pedido encontramos la palabra clave "navegador"
            hablar('Claro estoy en eso') ## escuharemos a nuestro asistente activo decir el siguiente mensaje
            webbrowser.open('https://www.google.com')## aquí solo vamos a abrir el navegador, pero no se realiza ninguna busqueda

        elif 'busca en internet' in pedido:
            ## la variable "termino" nos ayuda a lipiar lo que obtuvimos en pedido
            ## con "pedido.replace" al pasar como parametro "busca en internet", nos ayuda a quitar el comando/palabras clave de pedido
            ## como resultado vamos a tener " Tame Impala" y con ".strip()" nos ayuda a quitar los espacios, dejandonos con "Tame Impala"
            termino = pedido.replace('busca en internet', '').strip()
            ## mandamos a llamar a la función de hablar y segun el asistente activo, vamos a escuchar
            hablar(f'Buscando {termino} en internet') ## Busca en internet "Tame Impala"... según lo que hayamos encontrado en el pedido
            ## serpa el paramtero que se pasara
            pywhatkit.search(termino) ## con "pywhatkit.search" -> nos ayuda a hacer las busquedas,con esto podemos construir una liga de busqueda en internet
            ## sin tenerlo que hacer manualmente
            resultado = buscar_y_leer(termino) ## luego en la variable "resultado" mandamos a llamar a la función
            ##"buscar_y_leer" y le pasamos como parametro el termino, y ya con eso podemos leer
            if resultado: #3 decimos que si, en dado caso de que si hayamos podido leeer lo que encontramos en internet
                hablar('Esto es lo que encontré:') ## madamos a llamar a la función de hablar y dependiendo el asistente activo, escucharemos el siguiente mensaje
                hablar(resultado) ## igual se manda a llamar a la función hablar y pasamos a "resultado"
            else: ## en dado caso de no poder leer los resultado que obtuvimos
                hablar('Abrí el navegador pero no pude leer el resultado')
                ## llamamos a la función "hablar y vamos a escuchar el siguiente mensaje

        elif 'wikipedia' in pedido: ## si en "pedido" encontramos la palabra clave "wikipedia"
            hablar('Buscando en wikipedia') ## el asistente activo nos dira, el siguiente mensaje
## y bueno aquí tenemos una linea parecida a esta "  termino = pedido.replace('busca en internet', '').strip()"
            ## pero tenemos varia opciones en cadena, es decir que estas son las distintas formas en que podríamos pedir algo, si lo queremos de wikipedia
            termino = pedido.replace('busca en wikipedia', '') \
                .replace('busquen wikipedia', '') \
                .replace('busca wikipedia', '') \
                .replace('buscar en wikipedia', '') \
                .replace('wikipedia', '') \
                .replace('sobre', '') \
                .replace('qué es', '') \
                .replace('que es', '') \
                .strip()## todos los "\" indican uqe la linea continua, pero nos ayuda a darle continuidad a la instrución
            ##".replace" nos ayuda a quitar las palabra clave / comandos y dejr solo el termino, y con "strip" eliminamos los espacios que sobraron

            print(f"Término limpio: '{termino}'") ## se impirme en consola

            try: ## decimos que si vasmo a tratar de ejecuatr el siguiente bloque
                wikipedia.set_lang('es')## configuramos el idioma de wikipedia a español
                time.sleep(0.5)  # ← evita bloqueos de wikipedia, si hacemos pedidos muy seguidos, es una pausita
                resultado = wikipedia.summary(termino, sentences=2)
                ## en la variable "resulatdo" tenemos al metodo " wikipedia.summary" nos va ayudar a traer algunas oraciones de la busqueda
                ## el parametro "termino" nos indica que vamos a buscar y "sentences" nos indica cuantos reglones queremos
                hablar('Wikipedia dice que:') ## entonces el asistente activo nos va a decir que fue lo que encontro
                hablar(resultado) ## y nos lo va a decir

                ## except uno→ cuando hay varias páginas posibles para ese término
                # ejemplo: "jaguar" puede ser el animal, el carro o el sistema operativo
            except wikipedia.exceptions.DisambiguationError as e:
                try:## vamos a tratara de ejcutar el siguiente bloque:
                    # e.options[0] → toma automáticamente la primera opción de la lista y de esa opción nos trae las 2 primeros renglones
                    resultado = wikipedia.summary(e.options[0], sentences=2)
                    ## y traducimos el resultado a español
                    resultado = traducir_a_espanol(resultado)
                    ## y ya nuestro asistente activo nos dice lo que encontro en wikipedia en ese 1er resultado
                    hablar('Wikipedia dice que:')
                    hablar(resultado) ## y nos lo dice
                except:## en dado caso de que, no haya podido tomar una opción de todos los que encontro
                    ## nuestro asistente activo, nos va a decir el siguiente mensaje
                    hablar('Encontré varias opciones pero no pude precisar el tema')

                ### except dos → este except se ejecuta cuando la página no existe en español
                ### ejemplo: "Schnauzer" no tiene página en español
            except wikipedia.exceptions.PageError:
                # entonces por medio de la función "hablar" el sistente activo, nos va a decir el siguiente mensaje
                hablar('No encontré esa página en español, buscando en inglés')
                try:## entonces vamos a tratas de ejecuatr el siguiente bloque
                    wikipedia.set_lang('en') ## configuramos a wikipedia en ingles
                    resultado_en = wikipedia.summary(termino, sentences=2)
                    ## en la variable "resulatdo" tenemos al metodo " wikipedia.summary" nos va ayudar a traer algunas oraciones de la busqueda
                    ## el parametro "termino" nos indica que vamos a buscar y "sentences" nos indica cuantos reglones queremos
                    resultado = traducir_a_espanol(resultado_en) ## y como la busqueda fue en ingles, traducimos a español y lo guardamos en la
                    ## variable "resultado"
                    hablar('Wikipedia en inglés dice que:') ## y nuestro asistente activo por medio de la función de hablar nos va decir que encontro
                    hablar(resultado) ## y lo escuchamos
                except: ## en dado caso de no haber encontrado ninguna pagina, ni en ingles o no poder hacer la tradución
                    hablar('No encontré información sobre el tema')## nuestro asistente por medio del metododo hablar, nos dira que no encontro ningun resultado

            except Exception as e:## en dao caso de que no hayamos caigo en ninguno de estos except y no se haya podido haber hecho la busqueda
                print(f"Error wikipedia: {e}")  # ← se impirmie en consola, el error
                hablar('No encontré información sobre el tema') ## y nuestro asistente nos dice que no encontro nada del tema

        ## luego si en pedido encontramos la palabra clave "dia" o "día" con acento
        elif 'día' in pedido or 'dia' in pedido:
            pedir_dia()## madamos a llamar a la función "pedir_día()"

        ## luego si en pedido encontramos la palabra clave "hora"
        elif 'hora' in pedido :
            pedir_hora() ## y mandamos a llamar a la función "pedir_hora()"
###### __________________________
        ## cuandi decimos la frase clave "reproducir"/ "reproduce" y que sea detectada en el pedido
        elif 'reproducir' in pedido or 'reproduce' in pedido:
            ## mandamos a llamar a la función "hablar" y le pasamos como parametro, la siguinete frase
            hablar('Buena idea, voy a reproducir') ## lo vamos a escuchar con la voz de nuestro asistente activo
            pedido = pedido.replace('reproducir', '').strip()
            ## en la varibale "pedidio" vamos a limpiar el pedido, vamos a quitar las palabras clave por medio del metodo "replace"
            ## y le quitamos los espacios con ".strip()"
            pywhatkit.playonyt(pedido)## con pyehatkit, construimos una liga y pasamos como parametro "pedido", que pedido ya trae lo que queremos reproducir
            time.sleep(5) ## esta linea nos ayuda a esperar, antes de volver a hablar
            ## entonces en la variable "reproduciendo" que es  un booleando
            ## ese booleano nos lo devuelve la funcipon "modalidad_video()"
            reproduciendo= modalidad_video() ## y basicamente a lo que nos ayuda es a indicarle al
            ## usuario como llamar al asistente, bloquenado el ruido del sistema y solo activando el microfono,
            ## si escuha el nombre del asistente actual
###si en pedido encontramos la palabra clave "pausa", "pausar" o "stop"
        elif 'pausa' in pedido or 'pausar' in pedido or 'stop' in pedido:
            pyautogui.press('k')  # se presiona la tecla k
            reproduciendo = False ## y el booleano "reproduciendo" queda en "False"
            hablar('Video pausado, te escucho') ## y por medio de la función hablarnuestro asistente actual nos
            ## va a decir el siguinete mensaje
## si en pedido encontramos la palabra clave "play", "ponle" o "reanudar"
        elif 'play' in pedido or  'ponle' in pedido or 'reanudar' in pedido:
            time.sleep(5) ## vamos a dar un pasusa de 5 segundos, para que no se bloque la pagina
            pyautogui.press('k') ## y volvemos a presionar la tecla k, para reanudar el video
            reproduciendo = modalidad_video() ## reproduciendo que es un booleano toma el return de la función "modalidad_video()"
            ## linea 279

##si en pedido encontramos la palabra clave "siguiente"
        elif 'siguiente' in pedido:
            pyautogui.hotkey('shift', 'n')## ejecutamos el siguiente comando, que nos redireciona al siguiente video
            hablar('Siguiente video') ## por medio de la función "hablar" el asistente activo, nos va decir la siguiente frase
            reproduciendo = modalidad_video()## y mandamos a llamar a la función "modalida_video()" que nos va ayudar
            ## a saber como llamar al asistente cuando lo necesitemos y ademas pone a "reproduciendo" en TRUE

        elif 'subir volumen' in pedido:## si en pedido encontramos la palabra clave "subir volumen"
            for _ in range(8): ## vamos a presinar 8 veces la tecla de arriba
                pyautogui.press('up') ## aqui ejecutamos el comando de la tecla con la flechita arriba

        elif 'bajar volumen' in pedido or 'baja el volumen' in pedido: ## si en pedido encontramos "bajar volumen" o "baja volumen"
            for _ in range(8): ## vamos a presionar 8 veces la tecla de abajo
                pyautogui.press('down') ## aqui ejecutamos el comando de la tecla con la flechita abajo

        elif 'captura' in pedido or 'screenshot' in pedido: ## si encontramos la palabra clave "captura" o "screenshoot" en pedido
            screenshot = pyautogui.screenshot() ##en la variable "screenshot" vamos utilizar el metodo ".screenshoot()" de la libreria "pyautogui"
            nombre = f"captura_{datetime.datetime.now().strftime('%H%M%S')}.png"
            ## en la variable "nombre" vamos a formar el nombre con el que vamos a guardar la captura
            ## entonces traemos el metodod de "datetime" y de ahí ya obtenemos el momento con ".now" donde
            ## "H" correponde a hora, "M" a minuto y "S" a segundo
            screenshot.save(nombre) ## y luego en la variable Screenshot donde ya tenemos la captura, vamos a hacer un ".save" y a save le pasamos como parametro "nombre"
            ## uqe sera el nombre con el que guardaremos la captura
            hablar(f'Captura guardada como {nombre}') ## luego por medio de la función "hablar" nuestro asiste activo nos va adecir
            ##el siguiente mensaje junto con el nombre que se guardo la captura

        elif 'broma' in pedido: ## si en pedido encontramos la palabra clave "broma"
            try: ## vamos a tratas de ejecuat la siguinete linea
                hablar(pyjokes.get_joke('es')) ## y vamos a mandar a llamar a la función "hablar" y por medio del asistente activo
                ## vamos a traer al metodod ".get_jokes" de la libreria de "pyjokes" y pasamos como parametro "es" para que la broma sea en español
            except: ## en dado caso de que no se haya podido ejecutar la broma
                hablar('Uy, hoy no se me ocurre ninguna broma') ## por medio de la función hablar y el asistente activo en ese momento decimos
                ## el siguente mensaje

        elif 'calculadora' in pedido:## si en pedido encontramos la palabra clave "calculadora"
            ## con "subprocess.Popen" -> ejecuta un comando del sistema operativo desde el programa, es como si lo escribieramos en la terminal
            subprocess.Popen(['open', '-a', 'Calculator'])
                            #  ↑       ↑        ↑
                            #  │       │        └── nombre de la app a abrir
                            #  │       └── flag que significa "application"
                            #  └── comando de Mac para abrir cosas
            hablar('Abriendo calculadora') ## por medio de la función habalr y el asistente activo vamos a escuchar lo siguinete

        elif 'bloc de notas' in pedido: ## si en pedido encontramos la palabra clave "calculadora"
            ## con "subprocess.Popen" -> ejecuta un comando del sistema operativo desde el programa, es como si lo escribieramos en la terminal
            subprocess.Popen(['open', '-a', 'TextEdit'])
                            #  ↑       ↑        ↑
                            #  │       │        └── nombre de la app a abrir
                            #  │       └── flag que significa "application"
                            #  └── comando de Mac para abrir cosas
            hablar('Abriendo bloc de notas') ## por medio de la función habalr y el asistente activo vamos a escuchar lo siguinete

        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            ## en la variable accción, vamos a limpiar el pedido, entonces
            ##pedido = "precio de las acciones de apple"
            #.split('de')  → ['precio ', ' las acciones ', ' apple']
            #[-1]→' apple'← toma el último elemento
            #.strip() → 'apple'  ← quita espacios
            cartera = {'apple': 'AAPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'
                     } ## creamos un diccionario con las diferentes empresas como llave y con su valor odficial del wall stret
            try: ## tratamos de ejecutar el siguiente codigo
                accion_buscada = cartera[accion] ## en acción buscada, mandamos a llamar a "catera" y pasamos como parametro a acción
                ## que es la variable donde extraemos la empresa
                ticker = yf.Ticker(accion_buscada) # yf.Ticker() conecta con Yahoo Finance
                # y trae toda la información de esa acción
                precio_actual =  ticker.info['regularMarketPrice'] # de toda la información disponible
                # extrae solo el precio actual del mercado
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                ## y ya solo por medio de la función hablar y el asistente activo vamos a contruir un cadena de texto, donde pasamos como parametro
                ## la acción y el precio
            except: ## en dado caso de no haber podido encontrara la acción o ejecutar el bloque de codigo anterior
                hablar("Perdón pero no la he encontrado") ## mandamos a llamar a la función "hablar" y el asistente dice el siguiente mensaje


        elif 'adios' in pedido or 'adiós' in pedido: ## en dado caso de encontrar la palabra clave "adios" en pedido, vamos a :
            hablar('Hasta luego,vuelve pronto') ## el asistente nos dice el siguinete mensaje
            comenzar = False ## y el booleano comenzar se establece en "Falce"


        ## cuando en pedido encontramos la palabras clave "preguntale a la ia", "oye ia" y "pregunta" o "pregunta"
        elif 'pregúntale a la ia' in pedido or 'oye ia' in pedido or 'pregunta' in pedido:
            ## en la variable "pregunta" tenesmos varias opciones de como vamos a limpiar la pedido
            ## cada "\" nos indica las diferengtes formas en que queremos limpiar la petición
            ## dentro de cada ".replace" vamos a quitar las posibles palabras clave que dio el usuario
            pregunta = pedido.replace('pregúntale a la ia', '') \
                .replace('oye ia', '') \
                .replace('pregunta', '') \
                .strip() ## dejando solo la pregunta, que correponde a las comillas vacias,
            # que son llenados según lo que haya dicho el usuario seguido de la palabra clave y bueno con ".strip()" quitamos los espacios a la pregunta

            hablar('Déjame preguntarle a la IA') ## leugo el asistente por medio de la función hablar nos dice el siguinete mensaje
            respuesta = preguntar_a_ia(pregunta) ## entonces en respuesta vamos a mandar a llamar a la  función "pregunta_a_ia" y el pasamos como paramtero
            ## la variable regunta, que es la linea donde limpiamos al pedido
            if respuesta: ## si respuesta es True, osea que si se pudo ejecutar la función de " preguntar_a_ia(pregunta)", vamos a :
                hablar(respuesta)#por medio de la función hablar, vamos a pasar a "respuesta" y lo vamos a escuchar con la voz del asistente activo
            else: ## en dado caso de no haber obtenido un respuesta
                hablar('No pude obtener respuesta de la IA') ## el asistente dice el siguiente mensaje

        #####################################
        ## ahora aqui tenemos el cambio de los asistentes
        #####################################
        ## si en pedido encontramos las palabras clave como " cambia a Petunia" o peti¿unia en minuscula, entonces vamos a:
        elif 'cambia a Petunia' in pedido or 'cambia a petunia' in pedido:
            ## por medio de la instancia "nutria" vamos a mandar a llamar a:
            ##.root -> que es la ventanita que contiene al asistente
            ##.after -> lo usamos para correrlo en el 1er plano de tkinter
            ## el 0 -> nos indica que se ejecute en el hilo principal lo antes posible
            ## por medio de lambda, mandamos a llamar por medio de la instancia nutria a la función ".actualizar_personaje" y le pasamos como parametro a "nutria"
            ## gracias a lambda
            nutria.root.after(0, lambda: nutria.actualizar_personaje('nutria'))
            ## entonces una vez actualizado el asistente, por medio de la función hablar
            hablar('Hola, otra vez soy Petunia la nutria, tu asistente virtual!')## pEtunia nos dice esto
        ## pasa exactamente lo mismo con los otros 2 asistentes
        elif 'cambia a Rigoberto' in pedido or 'cambia a rigoberto' in pedido:
            nutria.root.after(0, lambda: nutria.actualizar_personaje('pato'))
            hablar('Cuack cuack, soy Rigoberto el pato, y tú asistente virtual!')

        elif 'cambia a Ramona' in pedido or 'cambia a ramona' in pedido:
            nutria.root.after(0, lambda: nutria.actualizar_personaje('jarifa'))
            hablar('Hola, soy Ramona la jirafa, tu asistente virtual!')
        ## entonces en dado caso de no poder cambiar de asistente, nos quedamos con nuestro asistente actual y nos
        else:## nos dice el siguiente mensaje
            hablar('No entendí tu pedido, intenta de nuevo')


"""
    Punto de entrada del programa.
    El 'if __name__' nos asegura que este bloque solo se ejecute
    cuando corremos asistente.py directamente, y no cuando
    otro archivo lo importa.

    El problema principal es que tkinter y el asistente
    no pueden correr en el mismo hilo porque se bloquean mutuamente:
        - tkinter necesita el hilo principal para la ventana y animaciones
        - pedir_cosas necesita su propio hilo para escuchar y responder

    La solución es correrlos en hilos separados:
        Hilo principal  → nutria.run()   (tkinter, ventana, animaciones)
        Hilo secundario → pedir_cosas()  (micrófono, pedidos, respuestas)
    """
if __name__ == '__main__':
    nutria = NutriaWidget() ## esta linea de aquí la utilizamos en lineas mas arriba,
    # pues basicamnete es una instancia del widget, que contiene la animación de nuestro asistente
    hilo = threading.Thread(target=pedir_cosas, daemon=True)
    # crea un hilo secundario para correr el asistente
    # target=pedir_cosas → función que correrá en ese hilo
    # daemon=True → si se cierra la ventana, el hilo muere automáticamente
    # evita que el programa siga corriendo en segundo plano
    hilo.start() # arranca el hilo secundario → pedir_cosas empieza a escuchar
    nutria.run()  # arranca tkinter en el hilo principal → muestra la ventana del asistente
    # este método se queda "bloqueado" aquí hasta que se cierra la ventana


