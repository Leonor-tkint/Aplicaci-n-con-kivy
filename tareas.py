from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

#Clase de la interfaz (muestra los datos visuales que tendrá la app)
class TareasApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Forma en la que se acomoda la barra
        self.orientation = 'vertical'
        self.padding = 10 #espacio interno entre los bordes del layout
        self.spacing = 10  # espacio entre elementos

        #Barra de escritura
        self.entrada = TextInput(
            hint_text="Escribe una tarea...",
            size_hint_y=None, #"size_hint_y=None" sirve para acomodar la barra de escritura, "None" tamaño fijo que uno decide (con width o height), es ahí donde se escribe "height=40"
            height=40
        )
        self.add_widget(self.entrada) #Se agrega el widget


        #Forma de los botones botones (alineados en una fila)
        botones = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40,
            spacing=10  # separa los botones
        )

        #Crear los botones
        #"on_press" acción que realizará el botón
        boton_agregar = Button(text="Agregar tarea", on_press=self.agregar_tarea)
        boton_eliminar = Button(text="Eliminar tarea", on_press=self.eliminar_tarea)
        boton_mostrar = Button(text="Mostrar tarea", on_press=self.mostrar_tarea)
        self.boton_editar = Button(text="Modificar tarea", on_press=self.editar_tarea) #cambio/agregar
   
        #Añadirlos al contenedor horizontal
        botones.add_widget(boton_agregar)
        botones.add_widget(boton_eliminar)
        botones.add_widget(boton_mostrar)
        botones.add_widget(self.boton_editar) 

        #Se añaden a la interfaz
        self.add_widget(botones)

        #Lista de tareas (con scroll por si son muchas)
        self.scroll = ScrollView()
        self.lista = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.lista.bind(minimum_height=self.lista.setter('height'))
        self.scroll.add_widget(self.lista)
        self.add_widget(self.scroll)

        #Variable para guardar la tarea seleccionada
        self.tarea_seleccionada = None
        self.modo_edicion = False #cambio/agregar

   #Función de los botones
    def agregar_tarea(self, instance=None):
        tarea = self.entrada.text.strip()
        if tarea:
            etiqueta = Label(text=tarea, size_hint_y=None, height=40)
            etiqueta.bind(on_touch_down=self.seleccionar_tarea)
            self.lista.add_widget(etiqueta)
            self.entrada.text = ""
        else:
            self.mostrar_popup("Advertencia", "Escribe una tarea antes de agregar.")



    def eliminar_tarea(self, instance=None):
        if self.tarea_seleccionada:
            self.lista.remove_widget(self.tarea_seleccionada)
            self.tarea_seleccionada = None
            self.modo_edicion = False 
        else:
            self.mostrar_popup("Advertencia", "Selecciona una tarea para eliminar.") #cambio/edicion



    def mostrar_tarea(self, instance=None):
        if self.tarea_seleccionada:
            self.mostrar_popup("Tarea seleccionada", self.tarea_seleccionada.text)
        else:
            self.mostrar_popup("Información", "No hay tarea seleccionada.")


    def editar_tarea(self, instance):
        if self.modo_edicion and self.tarea_seleccionada:
            nuevo_texto = self.entrada.text.strip()
            if nuevo_texto:
                self.tarea_seleccionada.text = nuevo_texto
                self.entrada.text = ""
                self.tarea_seleccionada = None
                self.modo_edicion = False
                self.boton_editar.text = "Modificar tarea"  #cambio
            else:
                self.mostrar_popup("Advertencia", "No puedes dejar la tarea vacía.")
        else:
            self.mostrar_popup("Información", "Selecciona una tarea antes de modificar.")
            

    def seleccionar_tarea(self, label, touch):
        if label.collide_point(*touch.pos): #Función para saber si hubo toque dentro del Label
            self.tarea_seleccionada = label
            self.entrada.text = label.text
            self.modo_edicion = True
            self.boton_editar.text = "Guardar cambios" 
        
    #Muestra un mensaje como el messagebox
    def mostrar_popup(self, titulo, mensaje):
        popup = Popup(
            title=titulo,
            content=Label(text=mensaje),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()
    
#Clase principal de la aplicación (crea la ventana)
class MiApp(App):
    def build(self):
        self.title="Administración de tareas" #Cambiar nombre de la aplicación
        return TareasApp()

# Ejecutar la app 
if __name__ == "__main__":
    MiApp().run()