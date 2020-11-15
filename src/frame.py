from datetime import datetime
import cv2
import numpy as np
import os
import traceback

RUTA_BASE = os.path.abspath(os.path.join(os.getcwd(), '..'))


nombre_video = "C0003"

# Abrir capturador en directo
cap = cv2.VideoCapture(0)

# Abrir capturador desde fichero de video grabado
cap = cv2.VideoCapture(os.path.abspath(os.path.join(RUTA_BASE, 'resources', 'videos', str(nombre_video) + '.MP4')))

count = 0
try:
    while cap.isOpened():
        read_flag, frame = cap.read()
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.abspath(os.path.join(RUTA_BASE, 'resources', 'frames', str(nombre_video) + '_' + str(count) + '.jpg')), frame)     # save frame as JPEG file
        count +=1

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

except Exception as e:
    print(print(f"[{datetime.now().strftime('%Y%m%d%H%M%S%f')}] --> Error grave durante la ejecucción"))
    traceback.print_exc()
finally:
        cap.release()
        cv2.destroyAllWindows()
