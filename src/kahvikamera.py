'''
Tämä ajetaan koneessa johon on kytkettynä kamera ja josta kuvat otetaan.
'''
import cv2
import numpy as np
import subprocess
import time
from datetime import datetime

def sendImageToServer():
    try:
        subprocess.run(['scp', 'kahvi.jpg','root@kattila.cafe:~/kahvikamera/static/images/'])
    except subprocess.CalledProcessError as e:
        print(f'An error occured: {str(e)}')

def mse(img1, img2):
   h, w = img1.shape
   diff = cv2.subtract(img2, img1)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

def check_difference():
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cap.read()
    cap.release()
    # Encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_data = np.array(img_encoded).tobytes()

    oldImage = cv2.imread('kahvi.jpg')

    img1 = cv2.cvtColor(oldImage, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    error = mse(img1, img2)

    print("MSE: ", error)
    if (error > 5): # Tämä on hattuvakio, jos bugeja niin tämä vahvasti epäiltynä syylliseksi.
        print("MSE yli 5, Kahvin tila muuttunut! Laitetaan uusi kuva.")
        cv2.imwrite('kahvi.jpg', frame)
        sendImageToServer()
    else:
        print("Kahvin tila ei muuttunut. ei tehdä mitään.")

def run_every_minute():
    while True:
        check_difference()
        time.sleep(5)

if __name__ == '__main__':
    run_every_minute()

