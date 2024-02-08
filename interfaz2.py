                        #### INTERFAZ GRAFICA ####
# librerias para la creacion de la interface

import tkinter as tk
'lib para crear interfaz grafica'
from tkinter import filedialog
'lib para abrir cuadros de dialogo' 

class ContadorPersonasApp:  # Define una clase llamada ContadorPersonasApp
    def __init__(self, root):  # Define el método __init__ que inicializa la clase
        self.root = root  # Establece el atributo 'root' de la clase como la ventana principal
        self.root.title("PROYECTO CONTADOR DE PERSONAS")  # Establece el título de la ventana
        self.root.geometry("500x350")  # Define el tamaño de la ventana
        self.root.configure(bg='black')  # Configura el color de fondo de la ventana como negro

        # Título principal
        self.title_label = tk.Label(root, text="PROYECTO CONTADOR DE PERSONAS", font=("Helvetica", 18), fg='white', bg='black')  
        # Crea una etiqueta con el título principal
        self.title_label.pack(pady=10)  # Empaqueta la etiqueta en la ventana

        # Nombre del creador
        self.name_label = tk.Label(root, text="Josue Balseca", font=("Helvetica", 12), fg='white', bg='black') 
        # Crea una etiqueta con el nombre del creador
        self.name_label.pack()  # Empaqueta la etiqueta en la ventana

        # Botones principales
        self.camera_button = tk.Button(root, text="Camara", command=self.open_camera_interface, font=("Helvetica", 14), bg='white', fg='blue')  
        # Crea un botón para abrir la interfaz de cámara
        self.camera_button.pack(pady=20)  # Empaqueta el botón en la ventana

        self.video_button = tk.Button(root, text="Video", command=self.open_video_interface, font=("Helvetica", 14), bg='white', fg='blue')  
        # Crea un botón para abrir la interfaz de video
        self.video_button.pack(pady=20)  # Empaqueta el botón en la ventana

        self.instrucciones_button = tk.Button(root, text="Instrucciones", command=self.show_instructions, font=("Helvetica", 14), bg='white', fg='blue')  
        # Crea un botón para mostrar las instrucciones
        self.instrucciones_button.pack(pady=20)  # Empaqueta el botón en la ventana

    def open_camera_interface(self):  # Define un método para abrir la interfaz de la cámara

        ###############################################################
#### Agrega aquí el código para la detección de objetos mediante la cámara ####
        pass

    def open_video_interface(self):  # Define un método para abrir la interfaz del video

        ###############################################################
#### Agrega aquí el código para cargar un video y realizar la detección de objetos ####
        pass

    def show_instructions(self):  # Define un método para mostrar las instrucciones
        # Puedes mostrar las instrucciones en una nueva ventana o en la consola
        instructions = "RECUERDE: LAS INSTRUCCIONES SON PARA AMBOS PROGRAMAS\n\n1. Presiona 'Camara' para iniciar la detección y conteo de personas desde la cámara.\n2. Presiona 'Video' para realizar la detección y conteo de un video.\n3. Dibuje las areas que desea contar. \n4. Presione 'N' para generar una nueva area. \n5. Presione 'C' si desea eliminar una linea del area. \n6. Presione 'Q' si desea salir de la interfaz de camara o video."
        tk.messagebox.showinfo("Instrucciones de Uso", instructions)  # Muestra un cuadro de mensaje con las instrucciones

if __name__ == "__main__":  # Verifica si el script está siendo ejecutado directamente
    root = tk.Tk()  # Crea una nueva ventana principal
    app = ContadorPersonasApp(root)  # Crea una instancia de la clase ContadorPersonasApp
    root.mainloop()  # Inicia el bucle principal de la aplicación