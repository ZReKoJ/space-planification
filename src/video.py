from datetime import datetime
import cv2
import numpy as np
import os

RUTA_BASE = 'C:\\Users\\enolg\\PycharmProjects\\Robots2\\'
FPS = 5

def cargar_histogramas(path):
    dict = {}
    for file in os.listdir(path):
        if file.endswith(".csv"):
            dict[file[:-4]] = np.genfromtxt(path  + file, delimiter=' ')
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
    return clase, min_distance


# Inicialización
histogramas = cargar_histogramas(RUTA_BASE)

# Abrir capturador en directo
cap = cv2.VideoCapture(0)

# Abrir capturador desde fichero de video grabado
nombre_video = "C0002"
cap = cv2.VideoCapture(f"{RUTA_BASE}{nombre_video}.MP4")
out = cv2.VideoWriter(f'output_{nombre_video}.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1920, 1080))

last_captured = None
w = 900

contador_errores = 0
try:
    while cap.isOpened():
        read_flag, frame = cap.read()
        if not read_flag:
            print(f"[{datetime.now().strftime('%Y%m%d%H%M%S%f')}] --> Error leyendo frame")
            contador_errores += 1
            if contador_errores == 5:
                break
        else:
            contador_errores = 0
            if last_captured is None or (datetime.now() - last_captured).microseconds > (1000000 / FPS):
                last_captured = datetime.now()

                hist = crear_histograma_img(frame)
                predict = predecir_imagen(hist, histogramas)
                cv2.putText(frame, predict[0], (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255))
                out.write(frame)
                img = cv2.resize(frame, (w, int(w * 1080 / 1920)))
                cv2.imshow("Video", img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

                print(f"[{datetime.now().strftime('%Y%m%d%H%M%S%f')}] --> {predict}")
except Exception as e:
    print(print(f"[{datetime.now().strftime('%Y%m%d%H%M%S%f')}] --> Error grave durante la ejecucción"))
    print(e)
finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()