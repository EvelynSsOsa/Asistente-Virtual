import tkinter as tk ## esta libreria nos sirve para poder crear interfaces, en esta caso para crear la ventanita de nuestro asistente
from PIL import Image, ImageTk ## esta nos sirve para poder trabajar con imagenes, para poder guardarlas
import threading


class NutriaWidget:
    ## bueno aquí tenemos el constructor de clase y basicamente en "init()" se ejecuta cuando creas el widget
    def __init__(self, personaje = 'nutria'): ## y ponemos por default al personaje nutria
        self.root = tk.Tk() ## esta es la ventana que contendra al asistente
        self.root.title("Petunia") ## le asignamos el titulo "Petunia" a la ventana (ESTA LINEA SE PODRÍA BORRAR,PERO CORRESPONDE A LAS 1ERA VERSIONES)
        self.root.overrideredirect(True) # sin barra de título, ni botones, para darle un aspecto más de un widget,
        self.root.attributes('-topmost', True)## esto nos permite que la ventana siempre permanezca arriba de otras ventanas
        self.root.lift()## trae a la ventana al frente inmediatamente
        self.root.attributes('-topmost', True)## y volvemos a aplicar la ventana encima de otras ventanas, para asegurarnos de ver al asistente siempre
        self.root.geometry('300x360+1100+600')# aquí estamos definiendo la posición en pantalla
        ## tenemos 300 pixeles de ancho por 360 de alto
        ##y con "1100+600" indicamos la posisción en donde queramos que salga nuestra ventana en cuanto a la superficie de la pantalla
        ## habalndo del eje y y el eje x

        # ── cargar las 3 imágenes para la nutria ────────────────────────────
        self.img_cerrada = ImageTk.PhotoImage(Image.open('cerrada.png')) ## boquita cerrada
        self.img_entreabierta = ImageTk.PhotoImage(Image.open('entreabierta.png')) ## boquita entreabierta
        self.img_abierta = ImageTk.PhotoImage(Image.open('abierta.png')) ## boquita abierta

        ### ─────────────cargando las 3 imagenes de la jarifita ─────────────
        self.img_jarifa_cerrada = ImageTk.PhotoImage(Image.open('jarifa_cerrada.png')) ## boquita cerrada
        self.img_jarifa_entreabierta = ImageTk.PhotoImage(Image.open('jarifa_entreabierta.png')) ## boquita entreabierta
        self.img_jarifa_abierta = ImageTk.PhotoImage(Image.open('jarifa_abierta.png'))## boquita abierta

        ### ─────────────cargando las 3 imagenes del patito─────────────
        self.img_pato_cerrado = ImageTk.PhotoImage(Image.open('pato_cerrado.png')) ## boquita cerrada
        self.img_pato_entreabierto = ImageTk.PhotoImage(Image.open('pato_entreabierto.png'))## boquita entreabierta
        self.img_pato_abierto = ImageTk.PhotoImage(Image.open('pato_abierto.png'))## boquita abierta


        # secuencia de imagenes para la animación de nutria cuando habla (Petunia)
        self.frames_hablar = [
            self.img_cerrada, ## 1ero tendra su boquita cerrada
            self.img_entreabierta, ## como la boquita se va abriendo para pronunciar palabras, sigue la imagen con la boquita entreabierta
            self.img_abierta, ## luego ya pronunciando palabras, abre su boquita por completo
            self.img_entreabierta, ## y la vuelve a cerrar para simular el efecto de que pronunciara otra palabra
        ]

        # secuencia de imagenes para la  animación de la jarifita cuando habla
        ## basicamente sigue el mismo orden que Petunia la nutria, solo que con los dinujitos de la jirafita
        self.frames_hablar_jarifa= [
            self.img_jarifa_cerrada,
            self.img_jarifa_entreabierta,
            self.img_jarifa_abierta,
            self.img_jarifa_entreabierta,
        ]

        # secuencia de imagenes para la  animación del patito cuando habla
        ## basicamente sigue el mismo orden que Petunia la nutria Y Ramona la Jarifita, solo que con los dinujitos de la jirafita
        self.frames_hablar_pato = [
            self.img_pato_cerrado,
            self.img_pato_entreabierto,
            self.img_pato_abierto,
            self.img_pato_entreabierto,
        ]

        # ── label de la imagen ───────────────────────────────
        self.label_img = tk.Label(self.root, bg='black') ## aquí vamos a crear una etiqueta vacia, en esta etiqueta
        ## es en donde vamos a poder ver a Petunia, Ramona o Rigoberto (ESTA LINEA ES DE LAS MÁS IMPORTANTES "self.label_img ") -> uso en linea 183
        self.label_img.pack() ## y bueno con esta linea colocamos la etiqueta dentro de la ventana

        # ── burbuja de texto ─────────────────────────────────
        ## esta nos sirve para ir viendo el texto que está diciendo el asistente
        ## este "self-label_burbuja" -> lo vamos a usar en la linea 184
        self.label_burbuja = tk.Label(
            self.root, ## entonces mandamos a llamar a nuestra ventana, que creamos arriba en la linea 9
            text='', ## como al principio nuestro asistente se queda unos segundo en silencio, text empieza en silencio
            bg='#1a1a2e', ## este será el color de la burbujita de texto, que es como color azul fuerte para que resalte la letra
            fg='white',## ponemos las letritas blancas
            font=('Helvetica', 11), ## le damos una fuente a las letras y un tamaño
            wraplength=270,##cuando el texto llegue a 270 píxeles de ancho hará salto de línea automáticamente
            justify='center', ## con esto queremos centrar el texto
            padx=10, ## damos espacio interno
            pady=8,
        )
        self.label_burbuja.pack(fill='x', padx=8, pady=4) ## con esta linea podemos colocar a la burbuja dentro de la ventana

        # ── botón cerrar ─────────────────────────────────────
        tk.Button( ## aqui creamos un boton
            self.root, ## y mandamos llamar a la ventana
            text='✕', ## decimos que como texto tenga un tachecito
            bg='#FF5555', ## este es el colo del botoncito
            fg='white', ## el color del tachecito
            bd=0,## la burbijita en esta ocasión no lleva ningun color de fondo
            font=('Helvetica', 14), ## aqui le damos una fuente y un tamaño al tachecito
            width=2,## definimos el ancho del boton
            command=self.root.destroy, ## cuando se presione el boton, se destruirá la ventana
            cursor='hand2',
        ).place(x=265, y=4) ## y esta es la posición del boton

        # ── arrastrar ventana ────────────────────────────────
        self.label_img.bind('<Button-1>', self.start_drag)
        ##Tkinter dispara <Button-1>, luego se ejecuta start_drag(event) y guarda dónde empezó el clic
        ##Mueves el ratón sin soltar el botón
        self.label_img.bind('<B1-Motion>', self.drag) ##Tkinter dispara repetidamente <B1-Motion>
        ##Se ejecuta drag(event) muchas veces, actualizando la posición de la ventana
        ##NOTA: Mientras arrastras, ese método calcula la nueva posición de la
        # ventana usando la diferencia entre la posición actual del cursor y la posición inicial guardada

        # ── estado inicial ───────────────────────────────────
        ##ESTA ES UNA DE LAS LINEAS MÁS IMPORTANTES
        self.hablando = False ##Inicializa una variable que representa el estado de habla del personaje, en este moneto esta en "False" pq así son los 2eros segundos del asistente
        self.frame_idx = 0 ## tomamos la 1era imagen de la animación, en este caso sera la imagen de la posición 0, es decir boquita cerrada
        self._anim_id = None ##guarda el ID del after() que programa la siguiente animación, se inicializa en None porque al arrancar no hay ninguna animación corriendo,
        ## El ID se genera en la linea 159

        self.actualizar_personaje(personaje) ##esta linea va a mostrar el valor del paramtero personaje, que tenemos en la función
        ## actualizar personaje
        ## Es decir el __init__ le pasa el valor de "personaje" a la función de "actualizar_personaje()" para que configure todo

        """__init__(personaje='nutria')
            ↓
        self.actualizar_personaje('nutria')
            ↓
        def actualizar_personaje(self, personaje):  # recibe 'nutria'
            self.personaje = personaje  # guarda 'nutria' 
        """

    # ── cambio de personaje ───────────────────────────────────
    def actualizar_personaje(self, personaje):
        """Cambia el personaje activo."""
        self.personaje = personaje
        ## dependiendo en donde haya caido personaje
        if personaje == 'nutria': ## si es nutria
           ## tenemos varias imagenes que vamos a relacionar con unas variables dependiendo que personjae hayas elegido
            self.img_actual_cerrada = self.img_cerrada ## entonces self.img_actual_cerrada, sera igual a la imagen de la boquita cerrada de la nutria
            self.img_actual_entreabierta = self.img_entreabierta## entonces "self.img_actual_entreabierta " sera igual a la imagen de la boquita entreabierta de la nutria
            self.frames_actuales = self.frames_hablar ## y aquí en "self_frames_actaules" seran igual a la lista de imagenes de la nutria "self.frames_hablar"
        elif personaje == 'pato': ## si toco pato:
            self.img_actual_cerrada = self.img_pato_cerrado ## ahora "self.img_actual_cerrada " sera igual a la imagen del patito con el piquito cerrado
            self.img_actual_entreabierta = self.img_pato_entreabierto ## ahora "self.img_actual_entreabierta" sera igual a la imagen del patito con el piquito entreabierto
            self.frames_actuales = self.frames_hablar_pato## y ahora "self.frames_actuales" sera igual a lista de imagenes que correponden al patito en este caso la lista es "self.frames_hablar_pato"
        elif personaje == 'jarifa': ## si toco jarifita:
            self.img_actual_cerrada = self.img_jarifa_cerrada## ahora "self.img_actual_cerrada " sera igual a la imagen de la jarifita con la boquita cerrada
            self.img_actual_entreabierta = self.img_jarifa_entreabierta ##ahora "self.img_actual_entreabierta" sera igual a la imagen de la jarifita con la boquita entreabierta
            self.frames_actuales = self.frames_hablar_jarifa## y ahora "self.frames_actuales" sera igual a lista de imagenes que correponden a la jarifita en este caso la lista es "self.frames_hablar_jarifa"
        self.mostrar_idle()  # muestra la imagen de boca cerrada

    # ── arrastre ─────────────────────────────────────────────
    """
            Guarda la posición inicial del cursor cuando el usuario
            hace clic sobre el personaje.
            El parámetro 'e' es el evento de tkinter que contiene
            las coordenadas del cursor en ese momento.
            """
    def start_drag(self, e):
        self._dx, self._dy = e.x, e.y
        #       ↑       ↑
        #       │       └── posición inicial en Y
        #       └──   posición inicial en X

    def drag(self, e):
        """
                Mueve la ventana mientras el usuario arrastra el cursor.
                Se ejecuta muchas veces por segundo mientras se arrastra.

                Calcula la nueva posición restando la posición inicial
                guardada en start_drag() a la posición actual del cursor:
                    nueva_x = posición_ventana + cursor_actual - cursor_inicial
                """
        x = self.root.winfo_x() + e.x - self._dx
        #    ↑ posición actual    ↑ cursor  ↑ cursor
        #    de la ventana        actual     inicial
        y = self.root.winfo_y() + e.y - self._dy
        self.root.geometry(f'+{x}+{y}') ### actualiza la posición de la ventana

    # ── estados ───────────────────────────────────────────────
    def mostrar_idle(self):

        """Muestra al personaje activo con la boca cerrada y
        limpia el texto de la burbuja.
        Se llama cuando el asistente termina de hablar o
        cuando se cambia de personaje.
        Usa self.img_actual_cerrada que fue configurada
        en actualizar_personaje()"""
        ## en la linea 63 creamos una etiqueta que es en donde iremos colocando la imagen de nuestros asistentes, le aplicamos el
        ##.confing y como parametro le pasamos la imagen que corresponde a las boquitas cerradas, que se configuraron en la función actualizar_personaje
        self.label_img.config(image=self.img_actual_cerrada)
        ## la etiqueta de la burbuja se crea por la linea 70 y con ayuda de ".confing"
        self.label_burbuja.config(text='') ## limpiamos la burbujita de texto, dejando a text vacio

    def mostrar_escuchando(self):

        """Muestra al personaje activo con la boca entreabierta
        y el texto 'Te escucho' en la burbuja.
        Se llama desde tranformar_audio_a_texto() en asistente.py
        cuando el micrófono está activo.
        Usa after(0) para ejecutarse en el hilo principal de tkinter."""
        ## mandamos a llamar a la ventana -> root
        ## luego pasamos "after" - nos indica que se ejecute en el hilo principal
        ##luego el 0 nos indica que lo tenemos que ejecutar lo antes posible
        ##lambda -> nos ayuda a poner en la etiqueta que creamos en la linea 63, la imagen del asistente que corresponde a
        ## boquita entre abierta
        self.root.after(0, lambda: (
            self.label_img.config(image=self.img_actual_entreabierta),
            self.label_burbuja.config(text='Te escucho... 🎙️', fg='#7EC8A0') ## luego en la etiqueta de la burbujita que creamos en la linea 70
        ))## establecemos el texto con el siguinte mensaje "te escucho" y las letras en color blanco con "fg='#7EC8A0'"

    # ── animación al hablar ───────────────────────────────────
    """
            Cicla por las imágenes de frames_actuales para simular
            el movimiento de la boca del personaje.
            Se llama a sí misma cada 180ms usando after() mientras
            self.hablando sea True.

            El % (módulo) hace que el índice vuelva a 0 cuando
            llega al final de la lista, creando un ciclo infinito:
            0 → 1 → 2 → 3 → 0 → 1 → 2 → 3 → ...
            cerrada → entreabierta → abierta → entreabierta → cerrada...
            """
    def _animar(self):
        ## Decimos que si "self.hablando" es negativo, es decir que ya no estamos hablando
        if not self.hablando:
            return ## regresamos lo siguiente
        frame = self.frames_actuales[self.frame_idx % len(self.frames_actuales)]
        """En la variable frame guardamos la imagen que queremos mostrar en ese momento. 
            La obtenemos de self.frames_actuales, que es la lista de imágenes del asistente
            activo (que configuramos en "actualizar_personaje()"). Para saber cuál imagen tomar,
            usamos self.frame_idx como contador que crece con cada llamada de _animar(). 
            El operador "%"(devuelve el residuo) junto con "len()" (cuenta los elementos de una lista) 
            se asegura de que ese contador nunca se salga del rango de la lista (0 al 3), haciendo que cuando llegue al final, vuelva a empezar 
            desde 0, logrando así el ciclo de animación: cerrada → entreabierta → abierta → entreabierta → cerrada."""
        self.label_img.config(image=frame) ## entonces una vez en la variable "frame" tenemos la imagen que queremos colocar en
        # la etiqeuta de la ventana "self.label_img", le aplicamos el ".confing" y le pasamos como parametro la variable frame
        self.frame_idx += 1 # avanza al siguiente frame de la lista
        self._anim_id = self.root.after(180, self._animar)
        #               ↑ guarda el ID aquí (SE CREA EN LA LINEA 109 Y SE ESTABLCE EN NONE) para poder cancelarlo en parar_habla()
        #                  180 = milisegundos entre cada frame, es decir que vamos a ejecutar esta función de "animar" cada 180 milesegundos

    def iniciar_habla(self, mensaje):
        """Llámala desde hablar() cuando Petunia empieza a hablar."""
        self.hablando = True ## al booleano "self.hablando" le cambiamos el valor a "TRUE"
        self.frame_idx = 0 ## tomamos la posición 0 de la lista de frames, por lo tanto por default comenzaremos con la boquita cerra
        texto = mensaje[:60] + ('...' if len(mensaje) > 60 else '') ## en la variable texto tenemos configurado como queremos que sea vea el texto en la burbuja
        ## entonces decimos que -> mensaje[:60] toma solo los primeros 60 caracteres del mensaje
        # luego la parte de ('...' if len(mensaje) > 60 else ''), en dado caso de que si haya mas de 60 caracteres al final agrega unos "..." y si la frase solo
        #y contienen 60 caracteres o menos, no agregar nada más
        ## luego mandamos a llamar la ventana con ".root" y decimos que queremos que corra en el hilo principal, y con el 0 decimos que lo queremos corriendo lo antes posible
        ## luego con "lambda" traemos a la etiqueta de burbuja, donde por medio de ".confing" pasamos como parametro la variable "texto", donde antes habiamos configurado, como queriamos
        ## el texto en la bubuja (linea239) y bueno ya por último con "fg=white" decimos que queremos que la letra sea blanquita
        self.root.after(0, lambda: (
            self.label_burbuja.config(text=texto, fg='white'),
            self._animar() ## por ultimo mandamos a llamar a animar ,para poder ir viendo los diferentes frames
        ))

    def parar_habla(self):
        """Llámala desde hablar() cuando Petunia termina de hablar."""
        self.hablando = False ## entonces tenemos un booleano que vamos a cambiar a "False"
        if self._anim_id:## decimos que si el último id que tenemos del ultimo frame que vimos en animación (existe/ se ejecuto)
            self.root.after_cancel(self._anim_id)## ## vamos a cancelar la corrida en el hilo principal, de este frama
        self.root.after(0, self.mostrar_idle) ## y ahora vamos a mostrar en la ventana ".root" y en el hilo principal ".after" y lo
        ##antes pisble con el 0, vamos a mostrar el frame de la boquita cerrada, que corresponde a "self.mostrar_idle" (esto fue configurado en "actualizar_personaje")

    def run(self):
        self.root.mainloop()
    ## Este método arranca el hilo principal de tkinter con mainloop(),
    ## que se queda "bloqueado" escuchando eventos (clicks, movimientos,
    ## actualizaciones de imagen y texto) hasta que se cierra la ventana.
    ## Se llama desde el bloque if __name__ == '__main__' después de
    ## arrancar el hilo secundario del asistente.
