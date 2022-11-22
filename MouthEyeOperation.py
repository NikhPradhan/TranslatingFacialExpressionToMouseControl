import Face_Indices
from cv2 import cv2
import LandmarksAndEucledianDistance
objEucledianDistance = LandmarksAndEucledianDistance.EucledianDistance()
objLandmark = LandmarksAndEucledianDistance.Landmark()
class EyeOperation:
    __shared_instance = None

    @staticmethod
    def getInstance():
        """Static Access Method"""
        if EyeOperation.__shared_instance == None:
            EyeOperation()
        return EyeOperation.__shared_instance

    def __init__(self):
        if EyeOperation.__shared_instance != None:
            raise Exception("Singleton class")
        else:
            self.BLINK_COUNT = 0
            self.EYES_CLOSED = 1
            self.EYES_OPENED = 0
            EyeOperation.__shared_instance = self

    def drawEye(self,frame,landmarks):
        leftEye = [objLandmark.getLmark(x, frame, landmarks) for x in Face_Indices.LEFT_EYE]
        rightEye = [objLandmark.getLmark(x,frame, landmarks) for x in Face_Indices.RIGHT_EYE]
        [cv2.circle(frame, x, 1, (255, 255, 0), 2) for x in leftEye]
        [cv2.circle(frame, x, 1, (255, 255, 0), 2) for x in rightEye]


    def drawEyeBrow(self,frame,landmarks):
        leftBrow = [objLandmark.getLmark(x,frame,landmarks) for x in Face_Indices.LEFT_EYEBROW]
        rightBrow = [objLandmark.getLmark(x,frame,landmarks) for x in Face_Indices.RIGHT_EYEBROW]
        [cv2.circle(frame, x, 1, (255, 255, 0), 2) for x in leftBrow]
        [cv2.circle(frame, x, 1, (255, 255, 0), 2) for x in rightBrow]

    def getEyeRatio(self,eye,frame,landmarks):
        """Get list of indices of specific eye and
        returns the ratio of vertical distance of the eye and horizontal distance of the eye """

        # topOfEye = landmarks[eye[12]]
        topOfEye = objLandmark.getLmark(eye[12], frame, landmarks)
        botOfEye = objLandmark.getLmark(eye[4], frame, landmarks)
        leftOfEye = objLandmark.getLmark(eye[0], frame, landmarks)
        rightOfEye = objLandmark.getLmark(eye[7], frame, landmarks)
        vDist = objEucledianDistance.getEuclDist(topOfEye, botOfEye)
        hDist = objEucledianDistance.getEuclDist(leftOfEye, rightOfEye)
        ratio = round(hDist / vDist, 2)
        return ratio

    def getEyeBrowRatio(self,frame,landmarks):
        distVE = objEucledianDistance.getEuclDist(objLandmark.getLmark(145, frame, landmarks),
                                               objLandmark.getLmark(52, frame, landmarks))  # vertical eyebrow and lower eye dist
        distHE = objEucledianDistance.getEuclDist(objLandmark.getLmark(133, frame, landmarks),
                                               objLandmark.getLmark(33, frame, landmarks))  # horizontal eyebrow and lower eye dist
        distRatioE = round(distVE / distHE, 2)
        return distRatioE

    def isBlink(self,val,frame,landmarks):
        leftEyeRatio = self.getEyeRatio(Face_Indices.LEFT_EYE,frame,landmarks)
        rightEyeRatio = self.getEyeRatio(Face_Indices.RIGHT_EYE,frame,landmarks)
        if val == 2:
            """blink of both eye """
            if leftEyeRatio > 6 and rightEyeRatio > 6:
                """ eyes closed
                EYES_OPENED is set to 0 because before closing eyes it was opened and its value was 
                 set to 1"""
                self.EYES_OPENED = 0
                self.EYES_CLOSED = 1
            else:
                """Eyes is opened"""
                self.EYES_OPENED = 1
            if self.EYES_OPENED == 1 and self.EYES_CLOSED == 1:
                """To check blink : first eye has to close i.e: EYES_CLOSED should be 1
                    and then EYES_OPENED should be 1.
                    """
                """HERE at every blink it updates the list with its time at SCROLLING_ACTIVE variable"""
                self.BLINK_COUNT += 1
                self.EYES_OPENED = 0
                self.EYES_CLOSED = 0
                return True
            else:
                return False
        elif val == 1:
            """Right eye close"""
            if leftEyeRatio <= 5.5 and rightEyeRatio > 5.5:
                return True
            else:
                return False
        else:
            """Left eye close"""
            if leftEyeRatio > 5.5 and rightEyeRatio <= 5.5:
                return True
            else:
                return False

class MouthOperation:

    __shared_instance = None
    @staticmethod
    def getInstance():
        """Static Access Method"""
        if MouthOperation.__shared_instance == None:
            MouthOperation()
        return MouthOperation.__shared_instance

    def __init__(self):
        if MouthOperation.__shared_instance != None:
            raise Exception("Singleton class")
        else:
            MouthOperation.__shared_instance = self




    def drawMouth(self,frame,landmarks):
        upperLip = [objLandmark.getLmark(x,frame, landmarks) for x in Face_Indices.UPPER_LIPS]
        lowerLip = [objLandmark.getLmark(x,frame, landmarks) for x in Face_Indices.LOWER_LIPS]
        [cv2.circle(frame, x, 1, (255, 255, 0), 2) for x in upperLip]
        [cv2.circle(frame, x, 1, (255, 255, 0), 2) for x in lowerLip]

    def getMouthRatio(self,frame,landmarks):
        distVM = objEucledianDistance.getEuclDist(objLandmark.getLmark(17, frame, landmarks), objLandmark.getLmark(0, frame, landmarks))
        distHM = objEucledianDistance.getEuclDist(objLandmark.getLmark(61, frame, landmarks), objLandmark.getLmark(291, frame, landmarks))

        distRatioM = round(distVM / distHM, 2)
        return distRatioM