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
        subprocess.run(['cp', 'kahvi.jpg','./static/images/'])
    except subprocess.CalledProcessError as e:
        print(f'An error occured: {str(e)}')

def mse(img1, img2):
   h, w = img1.shape
   diff = img1 - img2
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

    edges = detectEdges(frame) 

    print("MSE: ", error)
    if (error > 10): # Tämä on hattuvakio, jos bugeja niin tämä vahvasti epäiltynä syylliseksi.
        print("MSE yli 10, Kahvin tila muuttunut! Laitetaan uusi kuva.")
        cv2.imwrite('kahvi.jpg', edges)
        sendImageToServer()
    else:
        print("Kahvin tila ei muuttunut. ei tehdä mitään.")

def run_every_minute():
    while True:
        check_difference()
        time.sleep(5)

def detectEdges(image):
    height, width = image.shape[:2]
    roi = image[height // 2:, :]
    edges = cv2.Canny(roi, threshold1=80, threshold2=250)
    horizontal_kernel = np.ones((1, 6), np.uint8)
    vertical_kernel = np.ones((4, 2), np.uint8)
    dilated_edges = cv2.dilate(edges, vertical_kernel, iterations=1)
    eroded_edges = cv2.erode(dilated_edges, horizontal_kernel, iterations=1)
    contours, _ = cv2.findContours(eroded_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_edges = np.zeros_like(dilated_edges)
    for contour in contours:
        if cv2.arcLength(contour, True) > 250:
            # Draw the contour in the bottom half of the original image
            cv2.drawContours(image[height // 2:], [contour], -1, (255), thickness=cv2.FILLED)
            cv2.drawContours(filtered_edges, [contour], -1, (255), thickness=cv2.FILLED)
            

    # Iterate through rows in the eroded edges image to find the first and last rows with detected edges
    first_row = None
    last_row = None
    for row in range(filtered_edges.shape[0]):
        if np.any(filtered_edges[row, :]):
            if first_row is None:
                first_row = row
            last_row = row

    cv2.line(image, (width//2, height//2 + first_row), (width//2, height//2 + last_row), (0, 0, 255), 2)


    return image
    
if __name__ == '__main__':
    run_every_minute()

