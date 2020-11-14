import numpy as np
from cv2 import cv2
import os

RUTA_BASE = os.path.abspath(os.path.join(os.getcwd(), '..'))

def cargar_histogramas(path):
    dict = {}
    for file in os.listdir(path):
        if file.endswith(".csv"):
            dict[file[:-4]] = np.genfromtxt(os.path.abspath(os.path.join(path, file)), delimiter=' ')
    return dict

def crear_histograma_img(path):
    norm = np.empty(256)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    h, w = img.shape
    for i in range(256):
        norm[i] = hist[i][0] / (h * w)
    return norm

def predecir_imagen(histograma_img, histogramas):
    min_distance = None
    clase = None
    for key in histogramas:
        for hist in histogramas[key]:
            diff = histograma_img - hist
            diff = np.sqrt(sum(i ** 2 for i in diff))
            if min_distance is None or diff < min_distance:
                min_distance = diff
                clase = key
    return clase, min_distance

# Inicialización
histogramas = cargar_histogramas(os.path.abspath(os.path.join(RUTA_BASE, 'hist')))

test_file = open(os.path.abspath(os.path.join(RUTA_BASE, 'output', 'test.csv')), 'r') 
test_cases = test_file.readlines()
test_cases.sort()
test_file.close()

aciertos = 0

for line in test_cases:
    parsed = line.replace("\n", "").split(";")
    hist = crear_histograma_img(parsed[1])
    prediccion = predecir_imagen(hist, histogramas)
    if prediccion[0] == parsed[0]:
        aciertos += 1
    print(parsed[1], prediccion, prediccion[0] == parsed[0])

print(f"{aciertos / len(test_cases) * 100} % de aciertos")