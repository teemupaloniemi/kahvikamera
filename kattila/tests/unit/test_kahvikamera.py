import unittest
import cv2
import os
import kahvikamera

class TestImageDifference(unittest.TestCase):

    def test_mse_eroavatkuvat_eroavat(self):
        # Setup
        path = "/home/kattila/kahvicam/kahvikamera/kattila/tests/testdata/"
    
        imgA = cv2.imread(os.path.join(path, 'kahvi40proc.jpg'))
        imgB = cv2.imread(os.path.join(path, 'kahvi35proc.jpg'))
        imgA = kahvikamera.cv_preprocess(imgA)
        imgB = kahvikamera.cv_preprocess(imgB)

        result = kahvikamera.mse(imgA, imgB)

        self.assertNotEqual(result, 0.0)

    def test_mse_samatkuvat_eieroa(self):
        # Setup
        path = "/home/kattila/kahvicam/kahvikamera/kattila/tests/testdata/"
    
        imgA = cv2.imread(os.path.join(path, 'kahvi40proc.jpg'))
        imgB = cv2.imread(os.path.join(path, 'kahvi40proc.jpg'))
        imgA = kahvikamera.cv_preprocess(imgA)
        imgB = kahvikamera.cv_preprocess(imgB)

        result = kahvikamera.mse(imgA, imgB)

        self.assertAlmostEqual(result, 0.0, 1, "Samat kuvat eivät kuulu erota, mitävittua")


if __name__ == '__main__':
    unittest.main()