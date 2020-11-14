import numpy as np
from cv2 import cv2
import random
import os

RUTA_BASE = os.path.abspath(os.path.join(os.getcwd(), '..'))
X_TO_CSV = 60

f = open(os.path.abspath(os.path.join(RUTA_BASE, 'output', "test.csv")),'w')

# Get list of landmarks
landmarks = os.listdir(os.path.abspath(os.path.join(RUTA_BASE, 'resources')))
for landmark in landmarks:
    # Full Images path for a specific landmark
    images = os.listdir(os.path.abspath(os.path.join(RUTA_BASE, 'resources', landmark)))

    # We do choose only X_TO_CSV first paths for the CSV the others are for test
    random.shuffle(images)
    csv_images = images[:X_TO_CSV]
    test_images = images[X_TO_CSV:]

    histograms = np.empty((len(csv_images), 256))
    for i in range(0, len(csv_images)):
        p = os.path.abspath(os.path.join(RUTA_BASE, 'resources', landmark, csv_images[i]))
        img = cv2.imread(p , cv2.IMREAD_GRAYSCALE)
        hist = cv2.calcHist([img],[0],None,[256],[0,256])
        h,w = img.shape
        for j in range(256):    
            histograms[i][j] = hist[j][0] / (h * w)
        print(landmark, str(i + 1) + "/" + str(len(csv_images)))

    np.savetxt(os.path.abspath(os.path.join(RUTA_BASE, 'hist', landmark + ".csv")), histograms)
    for t in test_images:
        f.write(landmark + ";" + str(os.path.abspath(os.path.join(RUTA_BASE, 'resources', landmark, t))) + '\n')
        
f.close()