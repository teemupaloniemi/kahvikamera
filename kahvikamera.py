import cv2
from flask import Flask, request, Response
import numpy as np
import subprocess
import time
from datetime import datetime


app = Flask(__name__)

def scpkuvatoservu():
    try:
        subprocess.run(['scp', 'kahvi.jpg','root@172.232.159.94:~/kahvikamera/static/images/'])
    except subprocess.CalledProcessError as e:
        print(f'An error occured: {str(e)}')

def mse(img1, img2):
   h, w = img1.shape
   diff = cv2.subtract(img2, img1)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

@app.route('/kahvikamera', methods=['GET'])
def query_model():
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
    imgtmp = img2.copy()
    edges = cv2.Canny(frame, 100, 250)

    horizontal_kernel = np.ones((1,16), np.uint8)
    vertical_kernel = np.ones((6,1), np.uint8)
    # Dilate the edges. Dilation adds pixels to the boundaries of objects in an image.
    dilated_edges = cv2.dilate(edges, vertical_kernel, iterations=1)

    # Erode the dilated edges. Erosion removes pixels from the boundaries of objects in an image.
    # This can help to remove noise and small unwanted details.
    eroded_edges = cv2.erode(dilated_edges, horizontal_kernel, iterations=1)

    # Find the contours in the eroded edges image. Contours are simply the boundaries of the connected objects.
    # The function returns a list of contours and a hierarchy (which is not used here, hence the underscore).
    contours, _ = cv2.findContours(eroded_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty image (all zeros) with the same shape as the eroded edges image.
    # This will be used to draw the filtered contours.
    filtered_edges = np.zeros_like(dilated_edges)

    # Loop through each detected contour.
    for contour in contours:
        # Check if the length (perimeter) of the contour is greater than a threshold (100 in this case).
        if cv2.arcLength(contour, True) > 100:
            # Draw the contour on the filtered_edges image. The contour is filled with white (255).
            cv2.drawContours(imgtmp, [contour], -1, (180), thickness=cv2.FILLED)

    cv2.imshow("canny", imgtmp)
    cv2.waitKey(2)
    
    error = mse(img1, img2)

    print("MSE: ", error)
    if (error > 5): # Where does this 5 come from?
        print("MSE yli 5, Kahvin tila muuttunut! Laitetaan uusi kuva.")
        cv2.imwrite('kahvi.jpg', frame)
        scpkuvatoservu()
    else: 
        print("Kahvin tila ei muuttunut. ei tehdä mitään.")
    # Return image data in response with appropriate MIME type
    return Response(response=img_data, status=200, mimetype="image/jpeg")

def run_every_minute():
    while True:
        # Calling Flask route function directly is unusual and may not work in some setups.
        # Depending on the context, a different approach may be necessary.
        query_model()  
        time.sleep(5)  # wait one minute

if __name__ == '__main__':
#     app.run(debug=True, port=8000)

    # Start the periodic execution in a separate thread
    run_every_minute()

