import math
class EucledianDistance:
       def getEuclDist(self,pt1, pt2):
            """Return euclidean distance of two points"""
            dist = math.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)
            return int(dist)

class Landmark:
    def getLmark(self,index,frame,landmarks):
        """This function gets the index of the landmark and returns the x and y coordinates of that landmark in tuple"""
        fHeight = frame.shape[0]  # returns the height of the window
        fWidth = frame.shape[1]  # returns the Width of the window

        lm = (int((landmarks.landmark[index].x) * fWidth), int((landmarks.landmark[index].y) * fHeight))
        return lm