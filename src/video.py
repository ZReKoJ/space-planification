from datetime import datetime
import cv2
import numpy as np
import os
import traceback

RUTA_BASE = os.path.abspath(os.path.join(os.getcwd(), '..'))
FPS = 5
DELTA = 0.03

def cargar_histogramas(path):
    dict = {}
    for file in os.listdir(path):
        if file.endswith(".csv"):
            dict[file[:-4]] = np.genfromtxt(os.path.abspath(os.path.join(path, file)), delimiter=' ')
    return dict

def crear_histograma_img(img):
    norm = np.empty(256)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
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
    if min_distance < DELTA:
        return clase, min_distance
    return "None", min_distance

def esta_en_nodo(fotograma_actual, fotogramas_nodos):
    for key in fotogramas_nodos.keys():
        if fotograma_actual > fotogramas_nodos[key][0] and fotograma_actual < fotogramas_nodos[key][1]:
            return key
    return None

segundos_nodos = {'1_Entrada' : [0, 3],
                  '2_Cocina' : [14, 16],
                  '3_Pasillo' : [21, 24],
                  '4_Salon' : [32, 35],
                  '5_Grande' : [44, 47],
                  '6_Pequena' : [59, 63],
                  '7_Plantas' : [67, 74]}
fps = 50
fotogramas_nodos = {}
for key in segundos_nodos.keys():
    fotogramas_nodos[key] = [segundos_nodos[key][0] * fps, segundos_nodos[key][1] * fps]

# Inicialización
histogramas = cargar_histogramas(os.path.abspath(os.path.join(RUTA_BASE, 'hist')))

# Abrir capturador en directo
cap = cv2.VideoCapture(0)

# Abrir capturador desde fichero de video grabado
nombre_video = "C0002"
cap = cv2.VideoCapture(os.path.abspath(os.path.join(RUTA_BASE, 'resources', 'videos', str(nombre_video) + '.MP4')))
out = cv2.VideoWriter(os.path.abspath(os.path.join(RUTA_BASE, 'resources', 'videos', 'output_' + str(nombre_video) + '.avi')),cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1920, 1080))

last_captured = None
w = 900

contador_errores = 0
contador_fotogramas = 0
contador_correctos = 0
contador_erroneos = 0
# Contadores (tp, tn, fp, fn)
contadores = {'1_Entrada' : [0, 0, 0, 0],
                        '2_Cocina' : [0, 0, 0, 0],
                        '3_Pasillo' : [0, 0, 0, 0],
                        '4_Salon' : [0, 0, 0, 0],
                        '5_Grande' : [0, 0, 0, 0],
                        '6_Pequena' : [0, 0, 0, 0],
                        '7_Plantas' : [0, 0, 0, 0]}

try:
    while cap.isOpened():
        read_flag, frame = cap.read()
        contador_fotogramas += 1
        if not read_flag:
            print(f"[{datetime.now().strftime('%Y%m%d%H%M%S%f')}] --> Error leyendo frame")
            contador_errores += 1
            if contador_errores == 5:
                break
        else:
            contador_errores = 0
            nodo = esta_en_nodo(contador_fotogramas, fotogramas_nodos)
            if last_captured is None or (datetime.now() - last_captured).microseconds > (1000000 / FPS):
                last_captured = datetime.now()
                hist = crear_histograma_img(frame)
                predict = predecir_imagen(hist, histogramas)
                for key in contadores.keys():
                    if predict[0] != "None" and key != nodo and key != predict[0]:
                        contadores[key][1] += 1
                if nodo is not None:
                    if predict[0] != "None": 
                        if nodo == predict[0]:
                            contador_correctos += 1
                            contadores[nodo][0] += 1
                        else:
                            contador_erroneos += 1
                            contadores[nodo][3] += 1
                            contadores[predict[0]][2] += 1
                    cv2.putText(frame, f"{predict[0]} / {nodo}", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255))
                out.write(frame)
                img = cv2.resize(frame, (w, int(w * 1080 / 1920)))
                cv2.imshow("Video", img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                print(f"[{datetime.now().strftime('%Y%m%d%H%M%S%f')}] --> {predict}")
except Exception as e:
    print(print(f"[{datetime.now().strftime('%Y%m%d%H%M%S%f')}] --> Error grave durante la ejecucción"))
    traceback.print_exc()
finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

print("Estadisticas por nodo")
for nodo in contadores.keys():
    print(f"Matriz de confusión para el nodo {nodo}")
    print("         Predict")
    print("         +  | -")
    print("------------------")
    print(f"va | + | {contadores[nodo][0]} | {contadores[nodo][3]}") # tp | fp
    print("lu |--------------")
    print(f"e  | - | {contadores[nodo][2]} | {contadores[nodo][1]}") # fn | tp

    print(f"Accuracy: {(contadores[nodo][0] + contadores[nodo][1]) / (contadores[nodo][0] + contadores[nodo][1] + contadores[nodo][2] + contadores[nodo][3])}")
    print(f"Specificity: {contadores[nodo][1] / (contadores[nodo][1] + contadores[nodo][3])}")
    if contadores[nodo][0] + contadores[nodo][2] == 0:
        print("Sensitivity: NaN")
    else:
        print(f"Sensitivity: {contadores[nodo][0] / (contadores[nodo][0] + contadores[nodo][2])}")

print(f"Etiquetado correctamente: {contador_correctos}")
print(f"Etiquetado incorrectamente: {contador_erroneos}")
print(f"{contador_correctos / (contador_correctos + contador_erroneos) * 100} % de aciertos")