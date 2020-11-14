import numpy as np
from cv2 import cv2
import random
import os

import logging
import threading

RUTA_BASE = os.path.abspath(os.path.join(os.getcwd(), '..'))
X_TO_CSV = 80

def generateCSV(landmark, file, parse):
    # Full Images path for a specific landmark
    images = os.listdir(os.path.abspath(os.path.join(RUTA_BASE, 'resources', 'images', landmark)))

    # We do choose only X_TO_CSV first paths for the CSV the others are for test
    random.shuffle(images)
    csv_images = images[:parse]
    test_images = images[parse:]

    histograms = np.empty((len(csv_images), 256))
    for i in range(0, len(csv_images)):
        p = os.path.abspath(os.path.join(RUTA_BASE, 'resources', 'images', landmark, csv_images[i]))
        img = cv2.imread(p , cv2.IMREAD_GRAYSCALE)
        hist = cv2.calcHist([img],[0],None,[256],[0,256])
        h,w = img.shape
        for j in range(256):    
            histograms[i][j] = hist[j][0] / (h * w)
        print(landmark, str(i + 1) + "/" + str(len(csv_images)))

    np.savetxt(os.path.abspath(os.path.join(RUTA_BASE, 'hist', landmark + ".csv")), histograms)
    for t in test_images:
        f.write(landmark + ";" + str(os.path.abspath(os.path.join(RUTA_BASE, 'resources', 'images', landmark, t))) + '\n')
        
f = open(os.path.abspath(os.path.join(RUTA_BASE, 'output', "test.csv")),'w')
threads = list()

# Get list of landmarks
landmarks = os.listdir(os.path.abspath(os.path.join(RUTA_BASE, 'resources', 'images')))
for landmark in landmarks:
    # Open threads
    x = threading.Thread(target=generateCSV, args=(landmark, f, X_TO_CSV))
    threads.append(x)
    x.start()
    
# Wait for all threads
for index, thread in enumerate(threads):
    thread.join()

f.close()