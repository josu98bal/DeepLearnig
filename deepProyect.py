import tkinter as tk
from tkinter import filedialog
import cv2
import json
import numpy as np
from shapely.geometry import Polygon, Point
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import random

model = YOLO("models/yolov8n.pt", task="detect")
colors = random.choices(range(256), k=1000)

            ##### Clase principal del programa
class ContadorPersonasApp:

    def draw_results(self, image, image_results, areas, show_id=True):
        annotator = Annotator(image.copy())
        
        people_in_areas = {area_id: [] for area_id in areas.keys()}
        
        for result in image_results:
            for box in result.boxes:
                b = box.xyxy[0]
                cls = int(box.cls)
                conf = float(box.conf)
                label = f"{model.names[cls]} {round(conf*100, 2)}"
                if show_id and box.id is not None:
                    label += f' id:{int(box.id)}'
                
                    person_point = Point(box.xyxy[0][0], box.xyxy[0][1])
                    inside_area = any(area.contains(person_point) for area in areas.values())
                    
                    if cls == 0 and conf >= 0.35:
                        annotator.box_label(b, label, color=colors[int(box.id):int(box.id)+2] if box.id is not None else None)
                        
                        for area_id, self.area_polygon in areas.items():
                            if inside_area:
                                people_in_areas[area_id].append(int(box.id))
        
        for area_id, ids in people_in_areas.items():
            print(f"People in Area {area_id}: {len(ids)} with IDs {ids}")
        
        image_annotated = annotator.result()
        return image_annotated

    def get_viz(self, cam, points_cameras):
        cam_vis = cam.copy()
        alpha = 0.5
        overlay = cam.copy()
        for camid in self.points_cameras.keys():
            pts = np.array(self.points_cameras[camid], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(overlay, [pts], True, (0, 0, 255), thickness=3)
        cv2.addWeighted(overlay, alpha, cam_vis, 1 - alpha, 0, cam_vis)
        return cam_vis
###################################################################################
        ###########################################################################
                        #INICIALIZACION DE LAS FUNCIONES DE CAMARA#
    def visualize_camera(self):
        ret, camera_image_original = self.cap.read()
        if not ret:
            return None

        camera_image_visualization = self.get_viz(camera_image_original, self.points_cameras)
        cv2.imshow('video', camera_image_visualization)

    def mouse_camera(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN: 
            if not self.camera_index in self.points_cameras.keys():
                self.points_cameras[self.camera_index] = [[x, y]]
            else:
                self.points_cameras[self.camera_index].append([x, y])
            self.visualize_camera()

    def count_people_in_areas(self, frame, areas):
        results_track = model.track(frame, conf=0.40, classes=0, tracker="botsort.yaml", persist=True, verbose=False)
        
        for area_id, area_points in areas.items():
            self.area_polygon = Polygon(area_points)
            people_in_area = 0
            
            for result in results_track:
                for box in result.boxes:
                    person_point = Point(box.xyxy[0][0], box.xyxy[0][1])
                    if self.area_polygon.contains(person_point):
                        people_in_area += 1
            
            print(f"People in Area {area_id}: {people_in_area}")



#############################################
    
    def open_camera_interface(self):
        self.cap = cv2.VideoCapture(0)  # Usar la cámara del computador (puede necesitar ajustes dependiendo del número de cámara)

        camw_ = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        camh_ = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        ret, camera_image_original = self.cap.read()
        if not ret:
            print("Error al leer la cámara.")
            exit()

        cv2.namedWindow('video', cv2.WINDOW_NORMAL)
        # Especificar la posición y el tamaño de la ventana
        cv2.resizeWindow('video', 800, 600)  # Cambia los valores según tus necesidades
        cv2.setMouseCallback('video', self.mouse_camera)

        index = 0
        self.camera_index = 'Area' + f"--{index}"
        self.points_cameras = {}
        areas_to_count = {}
        count_people = False

        while True:
            self.visualize_camera()

            k = cv2.waitKey(1)
            if k == ord('q'):
                break
            elif k == ord('c'):
                if len(self.points_cameras[self.camera_index]) > 0:
                    self.points_cameras[self.camera_index] = self.points_cameras[self.camera_index][:-1]
                else:
                    print("La cámara no tiene más puntos")
                self.visualize_camera()
            elif k == ord('n'):
                index += 1
                self.camera_index = 'Area' + f"--{index}"
                self.points_cameras[self.camera_index] = []
            elif k == 13:  # Enter key
                areas_to_count = {k: Polygon(v) for k, v in self.points_cameras.items()}
                areas_to_draw = list(areas_to_count.values())
                count_people = True

            if count_people:
                break

        while True:
            ret, camera_image_original = self.cap.read()
            if not ret:
                break

            self.visualize_camera()

            self.count_people_in_areas(camera_image_original, areas_to_count)
            image_annotated = self.draw_results(camera_image_original, model(camera_image_original), areas_to_count)
            
            for area_id, self.area_polygon in areas_to_count.items():
                pts = np.array(self.area_polygon.exterior.coords, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image_annotated, [pts], True, (0, 255, 0), thickness=2)
                
                centroid = np.array(self.area_polygon.centroid.coords[0], np.int32)
                cv2.putText(image_annotated, f'Area {area_id}', tuple(centroid), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

            cv2.imshow('video', image_annotated)

            k = cv2.waitKey(1)
            if k == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

###################################################################################
        ###########################################################################
                        #INICIALIZACION DE LAS FUNCIONES DE VIDEO#
    def draw_results_video(self, image, image_results, areas, show_id=True):
        annotator = Annotator(image.copy())
        
        people_in_areas = {area_id: [] for area_id in areas.keys()}  # Inicializar la lista de IDs para cada área
        
        for result in image_results:
            for box in result.boxes:
                b = box.xyxy[0]
                cls = int(box.cls)
                conf = float(box.conf)
                label = f"{model.names[cls]} {round(conf*100, 2)}"
                if show_id and box.id is not None:  
                    label += f' id:{int(box.id)}'
                
                    # Check if the detected person is inside any of the selected areas
                    person_point = Point(box.xyxy[0][0], box.xyxy[0][1])
                    inside_area = any(area.contains(person_point) for area in areas.values())
                    
                    if cls == 0 and conf >= 0.35:
                        annotator.box_label(b, label, color=colors[int(box.id):int(box.id)+2] if box.id is not None else None)
                        
                        # Agregar la ID a la lista solo si la persona está dentro de alguna área
                        for area_id, area_polygon in areas.items():
                            if inside_area:
                                people_in_areas[area_id].append(int(box.id))
        
        for area_id, ids in people_in_areas.items():
            print(f"People in Area {area_id}: {len(ids)} with IDs {ids}")
        
        image_annotated = annotator.result()
        return image_annotated

    def get_viz_video(self, cam, points):
        """Función para obtener visualización con polígonos"""
        cam_vis = cam.copy()
        alpha = 0.5
        overlay = self.camera_image_original.copy()
        for camid in self.points_cameras.keys():
            pts = np.array(self.points_cameras[camid], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(overlay, [pts], True, (0, 0, 255), thickness=3)
        cv2.addWeighted(overlay, alpha, cam_vis, 1 - alpha, 0, cam_vis)
        return cam_vis

    def visualize_camera_video(self):
        """Función para visualizar la cámara"""
        camera_image_visualization = self.get_viz_video(self.camera_image_original, self.points_cameras)
        cv2.imshow('video', camera_image_visualization)

    def mouse_camera_video(self, event, x, y, flags, param):
        """Función ligada a la visualización de la cámara para realizar callbacks"""
        if event == cv2.EVENT_LBUTTONDOWN: 
            if not self.camera_index in self.points_cameras.keys():
                self.points_cameras[self.camera_index] = [[x, y]]
            else:
                self.points_cameras[self.camera_index].append([x, y])
            self.visualize_camera_video()

    def count_people_in_areas_video(self, frame, areas):
        results_track = model.track(frame, conf=0.40, classes=0, tracker="botsort.yaml", persist=True, verbose=False)
        
        for area_id, area_points in areas.items():
            area_polygon = Polygon(area_points)
            people_in_area = 0
            
            for result in results_track:
                for box in result.boxes:
                    person_point = Point(box.xyxy[0][0], box.xyxy[0][1])
                    if area_polygon.contains(person_point):
                        people_in_area += 1
            
            print(f"People in Area {area_id}: {people_in_area}")

    def open_video_interface(self):
        areas_to_count = {}  # Mover fuera del bucle
        areas_to_draw = []   # Nueva lista para almacenar áreas dibujadas

        count_people = False

        # Crear la ventana con un nombre específico
        cv2.namedWindow('video', cv2.WINDOW_NORMAL)

        # Especificar la posición y el tamaño de la ventana
        cv2.moveWindow('video', 100, 100)  # Cambia los valores según tus necesidades
        cv2.resizeWindow('video', 800, 600)  # Cambia los valores según tus necesidades

        video_path = "video.webm"  # Cambia a la ruta de tu video
        cap = cv2.VideoCapture(video_path)

        # Obtener el tamaño del frame del video
        camw_ = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        camh_ = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Leer el primer frame para la selección de áreas
        ret, self.camera_image_original = cap.read()
        if not ret:
            print("Error al leer el primer frame del video.")
            exit()

        cv2.namedWindow('video', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('video', self.mouse_camera_video)

        index = 0
        self.camera_index = 'Area' + f"--{index}"
        self.points_cameras = {}
        areas_to_count = {}
        count_people = False

        while True:
            self.visualize_camera_video()

            k = cv2.waitKey(1)
            if k == ord('q'):
                break
            elif k == ord('c'):
                if len(self.points_cameras[self.camera_index]) > 0:
                    self.points_cameras[self.camera_index] = self.points_cameras[self.camera_index][:-1]
                else:
                    print("La cámara no tiene puntos")
                self.visualize_camera_video()
            elif k == ord('n'):
                index += 1
                self.camera_index = 'Area' + f"--{index}"
                self.points_cameras[self.camera_index] = []
            elif k == 13:  # Enter key
                areas_to_count = {k: Polygon(v) for k, v in self.points_cameras.items()}  # Convert points to Polygons
                areas_to_draw = list(areas_to_count.values())  # Almacena las áreas dibujadas
                count_people = True

            if count_people:
                break

        # Continuar con la detección de personas en las áreas seleccionadas
        while True:
            ret, self.camera_image_original = cap.read()
            if not ret:
                break

            self.visualize_camera_video()

            self.count_people_in_areas_video(self.camera_image_original, areas_to_count)
            image_annotated = self.draw_results_video(self.camera_image_original, model(self.camera_image_original), areas_to_count)
            
            # Dibujar las áreas seleccionadas continuamente
            for area_id, area_polygon in areas_to_count.items():
                pts = np.array(area_polygon.exterior.coords, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(image_annotated, [pts], True, (0, 255, 0), thickness=2)
                
                # Agregar texto de identificación cerca del área
                centroid = np.array(area_polygon.centroid.coords[0], np.int32)
                cv2.putText(image_annotated, f' {area_id}', tuple(centroid), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

            cv2.imshow('video', image_annotated)

            k = cv2.waitKey(1)
            if k == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

#################################################################################################
######################## PAGINA PRINCIPAL DE LA INTERFAZ ########################################
        
    def __init__(self, root):
        self.root = root
        self.root.title("PROYECTO CONTADOR DE PERSONAS")
        self.root.geometry("600x400")  # Tamaño de la ventana
        self.root.configure(bg='black')  # Color de fondo

        # Título principal
        self.title_label = tk.Label(root, text="PROYECTO CONTADOR DE PERSONAS", font=("Helvetica", 18), fg='white', bg='black')
        self.title_label.pack(pady=10)

        # Nombre del desarrollador
        self.name_label = tk.Label(root, text="Josue Balseca", font=("Helvetica", 16), fg='white', bg='black')
        self.name_label.pack()

# Botones principales
        ## Boton de camara
        self.camera_button = tk.Button(root, text="Camara", command=self.open_camera_interface, font=("Helvetica", 14), bg='white', fg='blue')
        self.camera_button.pack(pady=20)
        ## Boton del video
        self.video_button = tk.Button(root, text="Video", command=self.open_video_interface, font=("Helvetica", 14), bg='white', fg='blue')
        self.video_button.pack(pady=20)
        ## Boton de instrucciones
        self.instrucciones_button = tk.Button(root, text="Instrucciones", command=self.show_instructions, font=("Helvetica", 14), bg='white', fg='blue')
        self.instrucciones_button.pack(pady=20)

################################################################

    def show_instructions(self):
        # Puedes mostrar las instrucciones en una nueva ventana o en la consola
        instructions = "RECUERDE: LAS INSTRUCCIONES SON PARA AMBOS PROGRAMAS\n\n1. Presiona 'Camara' para iniciar la detección y conteo de personas desde la cámara.\n2. Presiona 'Video' para realizar la detección y conteo de un video.\n3. Dibuje las areas que desea contar. \n4. Presione 'N' para generar una nueva area. \n5. Presione 'C' si desea eliminar una linea del area. \n6. Presione 'Q' si desea salir de la interfaz de camara o video."
        
        tk.messagebox.showinfo("Instrucciones de Uso", instructions)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContadorPersonasApp(root)
    root.mainloop()
