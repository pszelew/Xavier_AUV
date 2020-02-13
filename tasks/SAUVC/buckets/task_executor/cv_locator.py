import cv2 as cv
import numpy as np


def detectCircle(image):

    """
    :param param1: Upper threshold for the internal Canny edge detector
    :param param2: Threshold for center detection
    :param minRadius: Minimum radio to be detected. If unknown - zero as default.
    :param maxRadius: Maxium radio to be detected. If unknown - zero as default.
    """
    param1 = 50
    param2 = 30
    minRadius = 0
    maxRadius = 0

    circle = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 1, 20,
                             param1, param2, minRadius, maxRadius)
    return circle


def detectLines(image):
    linesP = cv.HoughLinesP(image, 1, np.pi / 180, 50, None, 50, 10)

    return linesP


def cannyEdges(image):
    lowThreshCanny = 0
    highThreshCanny = 255 * 2
    cv.Canny(image, lowThreshCanny, highThreshCanny)

    return image


def blurImage(image):
    cv.blur(image, (9, 9))

    return image


class BasketDetector:
    def __init__(self):
        pass

    color = "red"

    """
    Parameters used for threshold. Bottom and top values represented in HSV color model where
    H stands for hue
    S stands for saturation
    V stands for value
    Change of parameters may be needed due to conditions in pool (light etc.) 
    """
    lowHRed = 0
    highHRed = 179
    lowSRed = 0
    highSRed = 161
    lowVRed = 0
    highVRed = 112

    lowHBlue = 100
    highHBlue = 179
    lowSBlue = 0
    highSBlue = 255
    lowVBlue = 0
    highVBlue = 255

    kernel = np.ones((9, 9), np.uint8)

    def setLowThreshRed(self, lowHRed, lowSRed, lowVRed):
        self.lowHRed = lowHRed
        self.lowSRed = lowSRed
        self.lowVRed = lowVRed

    def setLowThreshBlue(self, lowHBlue, lowSBlue, lowVBlue):
        self.lowHBlue = lowHBlue
        self.lowSBlue = lowSBlue
        self.lowVBlue = lowVBlue

    def setHighThreshRed(self, highHRed, highSRed, highVRed):
        self.highHRed = highHRed
        self.highSRed = highSRed
        self.highVRed = highVRed

    def setHighThreshBlue(self, highHBlue, highSBlue, highVBlue):
        self.highHBlue = highHBlue
        self.highSBlue = highSBlue
        self.highVBlue = highVBlue

    def prepareImageRed(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        image = cv.inRange(image, np.array([self.lowHRed, self.lowSRed, self.lowVRed]),
                           np.array([self.highHRed, self.highSRed, self.highVRed]))
        image = self.doMorphOperations(image)
        image = blurImage(image)
        image = cannyEdges(image)
        return image

    def doMorphOperations(self, image):
        cv.erode(image, self.kernel, iterations=1)
        cv.dilate(image, self.kernel, iterations=1)
        cv.dilate(image, self.kernel, iterations=1)
        cv.erode(image, self.kernel, iterations=1)

        return image

    def prepareImageBlue(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        image = cv.inRange(image, np.array([self.lowHBlue, self.lowSBlue, self.lowVBlue]),
                           np.array([self.highHBlue, self.highSBlue, self.highVBlue]))
        image = self.doMorphOperations(image)
        image = blurImage(image)
        image = cannyEdges(image)
        return image

    def findCircleMiddlePoint(self, image):
        imageCloned = image

        """
        Checking whether basket is red or blue based on verifying if any circle was found
        for HSV set for red basket  
        """
        image = self.prepareImageRed(image)
        circle = detectCircle(image)

        if circle is None:
            image = self.prepareImageBlue(imageCloned)
            lines = detectCircle(image)

        return circle[0], circle[1]

    def checkColor(self, image):
        image = self.prepareImageRed(image)
        lines = detectLines(image)

        if lines is None:
            self.color = "blue"

        return self.color
