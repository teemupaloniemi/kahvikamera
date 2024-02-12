import cv2
import ffmpeg
import numpy as np
import subprocess
import time
from datetime import datetime
from enum import IntEnum
import os
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import kamera


class Loglevel(IntEnum):
    SILENT = 0
    ERROR = 1
    LOG = 2
    VERBOSE = 3
    DEFAULT = 0

def send_image_to_server(imgPath, loglevel = Loglevel.DEFAULT):
    try:
        subprocess.run(['scp', imgPath,'root@kattila.cafe:~/kahvikamera/web/static/images/'], capture_output=True).check_returncode()
    except Exception as e:
        log_error(f'An error occured 😔: {str(e)}', loglevel)

def whitebalance(img):
    wb = cv2.xphoto.createSimpleWB()
    outImg = wb.balanceWhite(img)
    return outImg

# Whitebalances outgoing image, writes image to 'kahvi.jpg'
def publication_postprocess(img, gatherdataset = False):
    timenow = time.strftime('%H:%M:%S')
    
    # Whitebalancing
    img = whitebalance(img)
    
    # for dataset (TODO move out)
    if (gatherdataset):
        path = "/home/kattila/kahvicam/kahvikamera/kattila/dataset"
        cv2.imwrite(os.path.join(path, timenow +'kahvi.jpg'), img)

    # Add timestamp
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.putText(img, timenow, (10,460), font, 2, (255,255,255), 5)

    # Lastly write to disk (outgoing file)
    cv2.imwrite('kahvi.jpg', img)

# Mean square error
def mse(img1, img2, loglevel = Loglevel.DEFAULT):
    s = time.time()
    h, w = img1.shape
    diff = img1 - img2
    err = np.sum(diff**2)
    ops = 3*h*w
    mse = err/(float(h*w))
    t = time.time() - s
    log_verbose(f"{ops} {t} {ops/t*10**12}", loglevel)
    return mse


def capture_camera_v4l2(kamera: kamera.Kamera) -> int:
    kamera.capture()


def capture_camera_cv2():
    # TODO capture longer exposed image for less noise (all my homies hate noise)
    # Ehdotettu yhdistää useamman capturen keskiarvo joka kyllä denoisee sen
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        ret, capImg = cap.read()

    finally:
        cap.release()

    return capImg


def retrieve_old_img(path):
    img = cv2.imread(path)
    return img

def cv_preprocess(raw):
    cvImg = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    return cvImg

def preprocess_capture(img):
    cv2.xphoto.dctDenoising(img, img, 8.0)
    return img

def log_verbose(str, loglevel = Loglevel.DEFAULT):
    if (loglevel >= Loglevel.VERBOSE):
        t = time.strftime('%H:%M:%S')
        print(f'LOG | {t:8} | {str}')

def log(str, loglevel = Loglevel.DEFAULT):
    if (loglevel >= Loglevel.LOG):
        t = time.strftime('%H:%M:%S')
        print(f'LOG | {t:8} | {str}')

def log_error(str, loglevel = Loglevel.DEFAULT):
    if (loglevel >= Loglevel.ERROR):
        t = time.strftime('%H:%M:%S')
        print(f'\033[1;31;40mERROR\033[1;37;40m | {t:8} | {str}')

def detectEdges(org):
    image = copy.deepcopy(org)
    
    edges = cv2.Canny(image, threshold1=80, threshold2=250)
    
    horizontal_kernel = np.ones((1, 6), np.uint8)
    vertical_kernel = np.ones((3, 2), np.uint8)
    
    dilated_edges = cv2.dilate(edges, vertical_kernel, iterations=1)
    eroded_edges = cv2.erode(dilated_edges, horizontal_kernel, iterations=1)
    contours, _ = cv2.findContours(eroded_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_edges = np.zeros_like(dilated_edges)

    for contour in contours:
        if cv2.arcLength(contour, True) > 250:
            # Draw the contour in the bottom half of the original image
            cv2.drawContours(filtered_edges, [contour], -1, (255), thickness=cv2.FILLED)
    return filtered_edges

def check_amount(img):
        # TODO Ei tää nyt oikee toimi :D 
        cropped_image = img[364:364+635,88:88+279] 
        avg = np.mean(cropped_image)
        start = 108
        step = 4
        if avg > 94:
            points_of_difference = (avg-start) / step
            return int(abs(points_of_difference)), avg
            # return int(min((max(0, 5-(points_of_difference) )), 5)), avg
        return 5, avg

def main():
    loglevel = Loglevel.VERBOSE
    # log_error("testi", loglevel)
    # cam = kamera.Kamera()
    #avgs = []
    #rets = []
    fig = plt.figure()
    #ax = fig.add_subplot(1, 1, 1)
    #ax2 = ax.twinx()

    # This is what iterates the whole shabang (its a delegate)
    def animate():#, avgs, rets):
        try:
            timenow = time.localtime()
            if timenow.tm_hour > 20 or timenow.tm_hour < 7:
                print("Kahvikamera is sleeping")
                time.sleep(600)
                return
            # cam.capture('testi-kahvi.jpg')
            # testImg = cv2.imread('testi-kahvi.jpg')
            # cv2.imshow(testImg)
            newImg = preprocess_capture(capture_camera_cv2())
            oldImg = retrieve_old_img("kahvi-local.jpg")

            cvNew = cv_preprocess(newImg)
            cvOld = cv_preprocess(oldImg)

            difference = mse(cvNew, cvOld)
            #edgeImg = detectEdges(newImg)
            #ax.clear()
            #ax2.clear()
        
            # running average
            #ret, avg = check_amount(cvNew)
            #avg_of_avg = avg
            #avg_of_ret = ret
            
            #if enough data
            #if len(avgs) > 3:
            #    avg_of_avg = (avgs[-1] + avgs[-2] + avg) / 3
            #if len(rets) > 3:
            #    avg_of_ret = (rets[-1] + rets[-2] + ret) / 3

            # There are databases for longer memory
            #if len(avgs) > 32:
            #    avgs.pop(0)
            #if len(rets) > 32:
            #    rets.pop(0)
                
            #avgs.append(avg_of_avg)
            #rets.append(avg_of_ret)
            
            #ax.plot(avgs, color='green', label='Kirkkaus')
            #ax2.plot(rets, color='blue', label='Kahvi')
            
            #log(f"Amount of coffee: {ret} / 5, avg: {avg}", loglevel) 
            log(f'MSE: {difference}')
            if (difference > 5):
                log("MSE yli 5, Kahvin tila muuttunut! Laitetaan uusi kuva. ☕", loglevel)
                cv2.imwrite('kahvi-local.jpg', newImg)
                publication_postprocess(newImg)
                send_image_to_server('kahvi.jpg', loglevel)
            else:
                log("Kahvin tila ei muuttunut. ei tehdä mitään. 🤷", loglevel)

        except Exception as ex:
            log_error(ex, loglevel)

        finally:
            time.sleep(2)

    while 1:
        animate()
    #ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
    #plt.show()

if __name__ == '__main__':
    main()
