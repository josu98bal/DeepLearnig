### El contenido se encuentra en 'master' Branch
### Proyecto de Deep Learning
# Detección de Objetos, Conteo de Personas y Parametrización de Áreas

Este proyecto consiste en una interfaz gráfica en Python que permite la detección de personas ya sea mediante la cámara del dispositivo o a través de un video seleccionado, se puede seleccionar areas que desees que realice el conteo de personas

## Descripción del Proyecto

Este proyecto representa el esfuerzo de investigación y desarrollo. Se enfoca en la aplicación de técnicas de deep learning para la detección de objetos y el conteo de personas en entornos de cámaras y videos seleccionados. Además, permite la parametrización de áreas de interés para análisis específicos.

## Objetivos Principales

1. **Detección de Objetos:** Se utiliza una combinación de modelos de detección de objetos, como YOLO (You Only Look Once), para identificar y localizar objetos en tiempo real y en videos seleccionados.

2. **Conteo de Personas:** Se implementan algoritmos especializados para contar de manera precisa el número de personas presentes en la escena, proporcionando métricas relevantes para análisis de ocupación y densidad.

3. **Parametrización de Áreas:** Permite definir áreas específicas en el campo de visión de las cámaras y calcular estadísticas detalladas sobre la ocupación y el comportamiento de los objetos detectados dentro de esas áreas.
## Requisitos

Python 3.x o superior

# Librerias
 - import tkinter as tk
 - from tkinter import filedialog
 - import cv2
 - import json
 - import numpy as np
 - from shapely.geometry import Polygon, Point
 - from ultralytics import YOLO
 - from ultralytics.utils.plotting import Annotator
 - import random

#### Estructura del Repositorio

- **`Readme.md`:** Descripción de la organización de archivos y directorios en la sección de models. Incluye detalles sobre la implementación y selección de modelos.

- **`camera.py`:** Script de la deteccion de objetos y conteo de personas en areas determinadas mediante el uso de una camara.

- **`video.py`:**  Script de la deteccion de objetos y conteo de personas en areas determinadas mediante un video.

- **`interfaz2.py`:**  Script de la deteccion de objetos y conteo de personas en areas determinadas mediante el uso de una camara.

- **`deepProyect.py`:** Script final unido todo los demas proyectos
## Uso

1. Ejecuta el script `deepProyect.py`.
2. En la pantalla principal, encontrarás un título y el nombre del creador.
3. Hay dos botones principales: "Camara" y "Video".
4. Al hacer clic en "Camara", se abrirá una interfaz para la detección y conteo de personas mediante la cámara.
5. Al hacer clic en "Video", se abrirá una interfaz para la detección y conteo de personas mediante un video
6. En ambas interfaces, presionando la letra 'Q' podra salir de las interfaces a la pantalla principal

## Documentacion
# para que sirve cada libreria

 -  cv2 (OpenCV): Utilizada para procesamiento de imágenes, visión por computadora y operaciones relacionadas con video.

 - json: Permite trabajar con datos en formato JSON, comúnmente utilizado para el intercambio de información entre aplicaciones.

 - numpy: Biblioteca eficiente para operaciones numéricas en Python, especialmente útil para trabajar con matrices y vectores.

 - shapely: Proporciona herramientas para realizar operaciones geométricas, como crear y manipular polígonos y puntos.

 - ultralytics.YOLO: Ultralytics es una librería para deep learning, y YOLO (You Only Look Once) es un algoritmo de detección de objetos eficiente.

 - ultralytics.utils.plotting.Annotator: Parte de Ultralytics, este módulo ayuda en la anotación y visualización de resultados de detección de objetos.

 - random: Permite generar números aleatorios, útil para tareas como la inicialización aleatoria en algoritmos de aprendizaje automático o selección aleatoria de elementos.

## Notas

- Asegúrate de tener instaladas las bibliotecas necesarias para la detección de objetos, como OpenCV.
- Personaliza el código según tus necesidades y preferencias.

#### Consideraciones de Diseño

- **Elección de Modelos:** Explicación de la elección de modelos de detección, justificando cómo se adaptan a los requisitos del proyecto.

- **Procesamiento de Datos:** Descripción detallada de las estrategias utilizadas para el preprocesamiento y manejo de datos.

- **Manejo de Resultados:** Información sobre cómo se gestionan y presentan los resultados, con consideraciones para su interpretación.

## Contribuciones

Se anima a los colaboradores a presentar problemas o sugerencias a través de issues y a contribuir con mejoras mediante pull requests.
