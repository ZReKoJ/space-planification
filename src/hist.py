import numpy as np
from cv2 import cv2
import glob


path = glob.glob("*.jpg")
images= np.empty((len(path),256))


for i in range(0,len(path)):
    img = cv2.imread(path[i] , cv2.IMREAD_GRAYSCALE)
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    h,w = img.shape
    for j in range(256):    
        images[i][j] = hist[j][0]/(h*w)
       
np.savetxt("dataset_hist.csv", images)
print('Total de imágenes procesadas: ', len(images))
