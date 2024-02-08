                    ### PROYECTO CONTADOR DE PERSONAS

## importacion librerias

import random  # Librería para generar números aleatorios
import cv2  # Librería para procesamiento de imágenes
import json  # Librería para manejar datos en formato JSON
import numpy as np # Librería para operaciones numéricas eficientes en Python
from shapely.geometry import Polygon, Point  # Librería Shapely para operaciones geométricas
from ultralytics import YOLO  # Ultralytics es una librería para deep learning y YOLO es un algoritmo de detección de objetos
from ultralytics.utils.plotting import Annotator  # Módulo Annotator de Ultralytics para la anotación y visualización de resultados


model = YOLO("models/yolov8n.pt", task="detect")

colors = random.choices(range(256), k=1000)
# genera una lista de 1000 colores aleatorios representados por RGB
def draw_results(image, image_results, areas, show_id=True):
    annotator = Annotator(image.copy())
    
    people_in_areas = {area_id: [] for area_id in areas.keys()}
    
    for result in image_results:
        for box in result.boxes:
            b = box.xyxy[0]  # Obtiene las coordenadas de la caja en formato xyxy
            cls = int(box.cls)
            conf = float(box.conf)  # Obtiene la confianza de la predicción y la convierte a punto flotante
            label = f"{model.names[cls]} {round(conf*100, 2)}"
            if show_id and box.id is not None:
                label += f' id:{int(box.id)}'
            
                person_point = Point(box.xyxy[0][0], box.xyxy[0][1])
                inside_area = any(area.contains(person_point) for area in areas.values())
                
                if cls == 0 and conf >= 0.35:
    # Comprueba si la clase es 'persona', la confianza es suficiente y está dentro de una de las áreas seleccionadas
                    annotator.box_label(b, label, color=colors[int(box.id):int(box.id)+2] if box.id is not None else None)
                    
                    for area_id, area_polygon in areas.items():
                        if inside_area:
                            people_in_areas[area_id].append(int(box.id))
    
    for area_id, ids in people_in_areas.items():
        print(f"People in Area {area_id}: {len(ids)} with IDs {ids}")
    # obtiene la imagen anotada y la retorna
    image_annotated = annotator.result()
    return image_annotated

def get_viz(cam, points_cameras): # Función para obtener una visualización con polígonos en la imagen de la cámara
    cam_vis = cam.copy()
    alpha = 0.5
    overlay = cam.copy()
# Itera sobre las cámaras y sus puntos para dibujar polígonos en la imagen
    for camid in points_cameras.keys():
        pts = np.array(points_cameras[camid], np.int32)
        pts = pts.reshape((-1, 1, 2))
# Combina la imagen original con los polígonos dibujados
        cv2.polylines(overlay, [pts], True, (0, 0, 255), thickness=3)
    cv2.addWeighted(overlay, alpha, cam_vis, 1 - alpha, 0, cam_vis)
    return cam_vis

# Función para visualizar la cámara
def visualize_camera():
    ret, camera_image_original = cap.read()
    if not ret:
        return None

    camera_image_visualization = get_viz(camera_image_original, points_cameras)
    cv2.imshow('video', camera_image_visualization)
# Función para manejar eventos de ratón en la visualización de la cámara
def mouse_camera(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: 
        if not camera_index in points_cameras.keys():
            points_cameras[camera_index] = [[x, y]]
        else:
            points_cameras[camera_index].append([x, y])
        visualize_camera()
# Función para contar personas dentro de áreas específicas en un frame
def count_people_in_areas(frame, areas):
    results_track = model.track(frame, conf=0.40, classes=0, tracker="botsort.yaml", persist=True, verbose=False)
# Itera sobre las áreas definidas    
    for area_id, area_points in areas.items():
        area_polygon = Polygon(area_points)
        people_in_area = 0
# Itera sobre los resultados de seguimiento y cuenta personas dentro del área        
        for result in results_track:
            for box in result.boxes:
                person_point = Point(box.xyxy[0][0], box.xyxy[0][1])
                if area_polygon.contains(person_point):
                    people_in_area += 1
# Imprime la cantidad de personas dentro del área        
        print(f"People in Area {area_id}: {people_in_area}")

cap = cv2.VideoCapture(0)  # Usar la cámara del computador (puede necesitar ajustes dependiendo del número de cámara)

camw_ = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
camh_ = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

ret, camera_image_original = cap.read()
if not ret:
    print("Error al leer la cámara.")
    exit()

cv2.namedWindow('video', cv2.WINDOW_NORMAL)
# Especificar la posición y el tamaño de la ventana
cv2.resizeWindow('video', 800, 600)  # Cambia los valores según tus necesidades
cv2.setMouseCallback('video', mouse_camera)

index = 0
camera_index = 'Area' + f"--{index}"
points_cameras = {}
areas_to_count = {}
count_people = False

while True:
    visualize_camera()

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('c'):
        if len(points_cameras[camera_index]) > 0:
            points_cameras[camera_index] = points_cameras[camera_index][:-1]
        else:
            print("La cámara no tiene más puntos")
        visualize_camera()
    elif k == ord('n'):
        index += 1
        camera_index = 'Area' + f"--{index}"
        points_cameras[camera_index] = []
    elif k == 13:  # Enter key
        areas_to_count = {k: Polygon(v) for k, v in points_cameras.items()}
        areas_to_draw = list(areas_to_count.values())
        count_people = True

    if count_people:
        break

while True:
    ret, camera_image_original = cap.read()
    if not ret:
        break

    visualize_camera()

    count_people_in_areas(camera_image_original, areas_to_count)
    image_annotated = draw_results(camera_image_original, model(camera_image_original), areas_to_count)
    
    for area_id, area_polygon in areas_to_count.items():
        pts = np.array(area_polygon.exterior.coords, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image_annotated, [pts], True, (0, 255, 0), thickness=2)
        
        centroid = np.array(area_polygon.centroid.coords[0], np.int32)
        cv2.putText(image_annotated, f'Area {area_id}', tuple(centroid), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    cv2.imshow('video', image_annotated)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()