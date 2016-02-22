import numpy as np
import cv2

print cv2.__version__

cap = cv2.VideoCapture(0)
while (cap.isOpened()):
    img = cap.read()
    cv2.ShowImage("camera",img)
    if cv2.WaitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.DestroyAllWindows()

