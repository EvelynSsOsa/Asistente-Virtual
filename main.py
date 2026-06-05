import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance
import pyjokes
import webbrowser
import datetime

### escuchar nuestro microfono y devolver el audio como texto
def tranformar_audio_a_texto():
    # almacenar el reconocedor en una variable
    r = sr.Recognizer()

    # configuracion del microfono
    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabación
        print("Ya puedes hablar :)")

        #guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            #buscar en google
            pedido = r.recognize_google(audio, language="es-mx")

            #prueba de que puedo ingresar y tranformar nuestra voz en un texto que se puede imprimir
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de no pueda realizar el pedido
        except sr.UnknownValueError:
            # prueba de que no comprendio el audio
            hablar("rayos creo que no entendí lo que dijiste")

            #devolver error
            return "sigo esperando"

        # en caso de no poder resolver el pedidio, es decir que se haya grabado el audio, pero no llo pudo traducir
        except sr.RequestError:

            # prueba de que no comprendio el audio
            hablar("rayos no hay servicio")

            # devolver error
            return "sigo esperando"

        ## error ineperado
        except:
            # prueba de que no comprendio el audio
            hablar("rayos, algo ha salido mal")

            # devolver error
            return "sigo esperando"


 ## función para que el asistente pueda ser escuchado
engine = pyttsx3.init()


 #Configuramos la voz una sola vez
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[101].id)  # Eddy (Español México)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def hablar(mensaje):

    #pronuciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

## informar el día de la semana
def pedir_dia():
    #craer variable con parametros
    dia = datetime.date.today()

    # crear variable para el día de la semana
    dia_semana= dia.weekday()
    print(dia_semana)

    ## diccionario con nombres de los dias
    calendario = {0:'Lunes',
                  1:'Martes',
                  2:'Miércoles',
                  3:'Jueves',
                  4:'Viernes',
                  5:'Sábado',
                  6:'Domingo'
                  }

    ## decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


## informar hora
def pedir_hora():
    ## crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)
    # decir la hora
    hablar(hora) ## aqui estamoa mandando a llamar a la función mientras le pasamos el paraemtro

# fucnión para el saludo inicial
def saludito():
    ## crear variable con datos de hora
    hora = datetime.datetime.now()
    # si todavia no son las 6 de la mañana, pero si soy mas de las 8 de la noche
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'##damos las buenas noches
    elif 6 <= hora.hour < 13: ## si hora es mayor a las 6 de la mañana y menor a la una de la tarde
        momento = 'Buen día' ## dmos los buenos días
    else: ## por descarte las buens tardes, else seran las buenas tardes ,es decir de un horario de la una a las 7 de la noche
        momento = 'Buenas tardes'

    hablar(f'{momento}, soy Petunia tú asistente personal, Por favor dime en que te puedo ayudar')

  # funcion central del asistente

def pedir_cosas():
    ## activar al saludo inicial
    saludito()

    #variable de corte
    comenzar = True
    ## loop central

    while comenzar:
    # activar el pedido
        pedido = tranformar_audio_a_texto().lower()

    if 'hola Petunia, me puedes' in pedido or 'gracias Petunia, me puedes' in pedido:
        if 'abrir youtube' in pedido:
            hablar('Con gusto estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
        elif 'abrir navegador' in pedido:
            hablar('Claro estoy en eso')
            webbrowser.open('https://www.google.com')

        elif 'que día es hoy' in pedido or 'que dia es hoy' in pedido or 'Qué día es hoy' in pedido:
            pedir_dia()

        elif 'qué hora es' in pedido or 'que hora es' in pedido or 'Qué hora es' in pedido :
            pedir_hora()

        elif 'adios' in pedido or 'adios' in pedido:
            hablar('Hasta luego,vuelve pronto')
            comenzar = False
        else:
            hablar('No entendí tu pedido, intenta de nuevo')





pedir_cosas()












