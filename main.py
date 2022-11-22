import autopy.mouse
from cv2 import cv2
import mediapipe as mp
import time
import numpy as np
import math
import pyautogui
import Face_Indices,LandmarksAndEucledianDistance,MouthEyeOperation
wCam,hCam = 640,480 #Bigger frame
#wCam,hCam = 300,200 #Shorter frame
wScr,hScr = autopy.screen.size()

#####################
"""Previous x and y loc and current x and y location"""
pLocX , pLocY = 0,0
cLocX , cLocY = 0,0
Mouth_OpenedClosed =0
####################
frame = 0
landmarks= 0

BLINK_COUNT =0
EYES_CLOSED=1
EYES_OPENED=0

SCROLLING_ACTIVE = [0,0,0,0,False] #for storing three successive blink's time stamp and second last index for no. of blinks till now
                                    # and last for Flag
MOUTH_ACTIVE = [0,0,False]

MOUTH_OPENED = 0
"""Cap is the object for video either here its the webcam """
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
###################### Object calling###################

##############################################################
if cap.isOpened():
    pTime=0
    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    FaceMesh = mpFaceMesh.FaceMesh()

def getLmark(index):
    """This function gets the index of the landmark and returns the x and y coordinates of that landmark in tuple"""
    global frame
    global landmarks
    fHeight = frame.shape[0] # returns the height of the window
    fWidth = frame.shape[1]  # returns the Width of the window

    lm=(int((landmarks.landmark[index].x)*fWidth),int((landmarks.landmark[index].y)*fHeight))
    return lm

def mainFunction():
    """Further calls various functions according to its detection"""
    global frame
    global BLINK_COUNT
    global SCROLLING_ACTIVE
    global MOUTH_ACTIVE
    objEyeOperation = MouthEyeOperation.EyeOperation.getInstance()
    objMouthOperation = MouthEyeOperation.MouthOperation.getInstance()
    #objMouthOperation = MouthEyeOperation.MouthOperation(frame, landmarks)

    if(MOUTH_ACTIVE[2]==False and SCROLLING_ACTIVE[4]==False):
        """ This is a normal Mode Where both CursorMove Mode and scrolling is deactive """

        if objMouthOperation.getMouthRatio(frame,landmarks)<0.6:
            draw_text(frame, f'blink count: {objEyeOperation.BLINK_COUNT} ', pos=(400, 50), font_scale=1, text_color=(0, 0, 255),font_thickness=1)
        draw_text(frame, f' Normal mode: ', pos=(160, 30), font_scale=1, text_color=(255, 255, 255),
                  font_thickness=1)

        draw_text(frame, f'1. Blink Thrice: Scrolling Mode', pos=(20, 60), font_scale=1,text_color=(255, 255, 255), font_thickness=1)
        draw_text(frame, f'2. Open Mouth(3Secs) : CursorMove Mode', pos=(20, 80), font_scale=1, text_color=(255, 255, 255),font_thickness=1)
        objEyeOperation.drawEye(frame,landmarks)
        objMouthOperation.drawMouth(frame,landmarks)
    if(objEyeOperation.isBlink(2,frame,landmarks) and MOUTH_ACTIVE[2]==False):
            """If blink is done then it updates the value in scrolling_active array accordingly"""
            """Here this block is executed only if mouse move mode is deactivated i.e MOUTH_ACTIVE[2] is Fasle """
            #FIRST BLINK
            if(SCROLLING_ACTIVE[3]==0):
                SCROLLING_ACTIVE[0] = round(time.time(),2)
                SCROLLING_ACTIVE[3]+=1
            #SECOND BLINK
            elif( SCROLLING_ACTIVE[3]==1):
                SCROLLING_ACTIVE[1] = round(time.time(),2)
                SCROLLING_ACTIVE[3]+=1

            #THIRD BLINK
            elif(SCROLLING_ACTIVE[3]==2):
                SCROLLING_ACTIVE[2] = round(time.time(),2)
                SCROLLING_ACTIVE[3]+=1

            #If blink is more than 3 but scrolling hasn't been activated
            elif(SCROLLING_ACTIVE[3]>=3):
                SCROLLING_ACTIVE[0]= SCROLLING_ACTIVE[1]
                SCROLLING_ACTIVE[1]= SCROLLING_ACTIVE[2]
                SCROLLING_ACTIVE[2]= round(time.time(),2)
                SCROLLING_ACTIVE[3]+=1



            if(abs(SCROLLING_ACTIVE[2]-SCROLLING_ACTIVE[0])!=0 and abs(SCROLLING_ACTIVE[2]-SCROLLING_ACTIVE[0]) < 0.8 ):
                """If the third blink's time - 1st blink time is less than 0.8sec then activate scrolling and reset the SCROLLING_ACTIVE"""
                if (SCROLLING_ACTIVE[4] == False):
                    SCROLLING_ACTIVE[4] = True #set to True and if again blink 3 times then it should be deactivateScrolling
                else:
                    SCROLLING_ACTIVE[4] = False
                '''Reset the SCROLLING_ACTIVE'''
                SCROLLING_ACTIVE[0] = 0
                SCROLLING_ACTIVE[1] = 0
                SCROLLING_ACTIVE[2] = 0
                SCROLLING_ACTIVE[3] = 0

    """if want to check the value uncomment"""
    #cv2.putText(frame, f'{MOUTH_ACTIVE[0]} {MOUTH_ACTIVE[1]} {MOUTH_ACTIVE[1]-MOUTH_ACTIVE[0]} \n {MOUTH_ACTIVE[2]}', (70, 70), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
    #cv2.putText(frame, f'blink count: {BLINK_COUNT} ', (200, 50), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

    ##################
    """for activating mouse move mouth has to be opened constantly for atleast 2 secs
    so detecting the mouth open """
    if SCROLLING_ACTIVE[4] == False:
        if objMouthOperation.getMouthRatio(frame,landmarks) > .60 :
            """Mouth open"""

            draw_text(frame, f'Mouth Open : {MOUTH_ACTIVE[1] - MOUTH_ACTIVE[0]} secs', pos=(380,50), font_scale=1,
                      text_color=(0, 0, 255), font_thickness=1)

            if MOUTH_ACTIVE[0]==0:
                MOUTH_ACTIVE[0]=abs(int(time.time()))%100

            else:
                MOUTH_ACTIVE[1]=abs(int(time.time()))%100
        else:
            """If mouth closed then reset"""
            MOUTH_ACTIVE[:2] = [0] * 2

        if ((MOUTH_ACTIVE[1]-MOUTH_ACTIVE[0])!=0 and (MOUTH_ACTIVE[1]-MOUTH_ACTIVE[0]) >= 3) :

            if MOUTH_ACTIVE[2] == False:
                MOUTH_ACTIVE[2] = True
            else:
                MOUTH_ACTIVE[2]=False
            MOUTH_ACTIVE[:2] = [0] * 2

    if SCROLLING_ACTIVE[4] == True and MOUTH_ACTIVE[2] == False:
        activateScrolling()
    elif MOUTH_ACTIVE[2] == True and SCROLLING_ACTIVE[4] == False:
        activateCursor()
    ############


"""If scrolling false then mouse hover else scrolling"""
def activateScrolling():

    """IF eye blink more than three times in less than .8 sec then activate

    Scroll up eyebrow top and bottom-eyelid distance increase then decrease y axis
    scroll down if lower lips mid index and upper lips mid index distance increase y axis increase
    """
    global frame
    global landmarks
    objEyeOperation = MouthEyeOperation.EyeOperation.getInstance()
    objMouthOperation = MouthEyeOperation.MouthOperation.getInstance()
    #cv2.putText(frame, f'blink count: {BLINK_COUNT} ', (400, 50), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
    draw_text(frame, f'blink count: {BLINK_COUNT} ', pos=(400, 50), font_scale=1,
              text_color=(0, 0, 255), font_thickness=1)
   # cv2.putText(frame, f' Scrolling  mode: ', (200, 30), cv2.FONT_ITALIC, .7, (0, 0, 0), 2)
    draw_text(frame, f' Scrolling  mode: ', pos=(200, 30), font_scale=1,
              text_color=(0, 0, 255), font_thickness=1)

    #cv2.putText(frame, f'1. Scroll Up : eyebrow up', (20, 60), cv2.FONT_ITALIC, .6, (0, 255, 255), 2)
    draw_text(frame, f'1. Scroll Up : eyebrow up', pos=(20, 60), font_scale=1,
              text_color=(0, 255, 255), font_thickness=1)

    #cv2.putText(frame, f'2. Scroll down : open mouth', (20, 80), cv2.FONT_ITALIC, .6, (0, 255, 255), 2)
    draw_text(frame, f'2. Scroll down : open mouth', pos=(20, 80), font_scale=1,
              text_color=(0, 255, 255), font_thickness=1)

    #cv2.putText(frame, f'3. Blink Thrice: Normal Mode', (20, 100), cv2.FONT_ITALIC, .6, (0, 255, 255), 2)
    draw_text(frame, f'3. Blink Thrice: Normal Mode', pos=(20, 100), font_scale=1,
              text_color=(0, 255, 255), font_thickness=1)
    objEyeOperation.drawEye(frame,landmarks)
    objMouthOperation.drawMouth()
    objEyeOperation.drawEyeBrow(frame,landmarks)



    #cv2.putText(frame,f'ratioEye: {str(distRatioE)} ratioM {str(distRatioM)}' ,(200,100),cv2.FONT_ITALIC,1,(0,0,255),1)
    if objEyeOperation.getEyeBrowRatio(frame,landmarks) > .92:
        """ Scroll up"""
        cv2.line(frame, getLmark(153), getLmark(65), (0, 0, 255), 1)
        cv2.line(frame, getLmark(133), getLmark(33), (0, 0, 255), 1)
        pyautogui.scroll(20)
    elif objMouthOperation.getMouthRatio() > .60:

        """Scroll down"""
        pyautogui.scroll(-20)
        cv2.line(frame,getLmark(17),getLmark(0),(0,0,255),1)

    #cv2.circle(frame,landmarks[291],1,(0,255,0),1)
    #cv2.circle(frame,landmarks[61],1,(0,255,0),1)

    """If want to check the value uncomment"""
    #cv2.putText(frame, str(distVM), (200, 300), cv2.FONT_ITALIC, 1, (0, 0, 255), 1)




def activateCursor():
    """Mouse Cursor control """
    objEyeOperation = MouthEyeOperation.EyeOperation.getInstance()
    objMouthOperation = MouthEyeOperation.MouthOperation.getInstance()
    draw_text(frame, " Cursor Control mode: ", pos=(160, 30), font_scale=1,text_color=(0, 0, 255), font_thickness=1)
    draw_text(frame, f' Move nose within pink box ', pos=(220, 300), font_scale=1,text_color=(255, 0, 255), font_thickness=1)
    draw_text(frame, f'1. Left click : Left eye blink', pos=(20, 60), font_scale=1,text_color=(0, 255, 0), font_thickness=1)
    draw_text(frame, f'2. Open Mouth(3Secs) : Normal Mode', pos=(20, 80), font_scale=1,text_color=(0, 255, 0) ,font_thickness=1)

    ####################################
    global pLocX,pLocY,cLocY,cLocX
    smoothValue = 10
    nosex, nosey = getLmark(4)
    global MOUTH_OPENED
    ############################

    objEyeOperation.drawEye(frame,landmarks)
    objMouthOperation.drawMouth(frame,landmarks)
    cv2.circle(frame,(nosex,nosey),2,(0,0,255),1)

    ###################################################################################
    """For shorter frame uncomment this and also wCam and hCam value at the top"""
    #cv2.rectangle(frame, (170, 140), (wCam - 210, hCam - 100), (255, 0, 255), 2)
    #x1 = np.interp(nosex, (170, wCam - 210), (0, wScr))
    #y1 = np.interp(nosey, (140, hCam - 100), (0, hScr))

    ##################################################################################
    """For bigger frame uncomment this and also wCam and hCam value at the top"""
    #cv2.rectangle(frame,(230,220),(wCam - 310, hCam -200),(255,0,255),2)
    cv2.rectangle(frame, (220, 220), (wCam - 300, hCam - 200), (255, 0, 255), 2)
    x1 = np.interp(nosex, (220, wCam-300), (0, wScr))
    y1 = np.interp(nosey, (220, hCam-200), (0, hScr))

    cLocX = pLocX + (x1 - pLocX) / smoothValue
    cLocY = pLocY + (y1 - pLocY) / smoothValue
    autopy.mouse.move(cLocX, cLocY)

    pLocX , pLocY = cLocX , cLocY

    if (objEyeOperation.isBlink(0,frame,landmarks)):
        """both eye blink to left click"""
        autopy.mouse.click()


    #cv2.circle(frame,nosex,nosey,(255,255,0))
    #print(nosex,nosey)

def draw_text(img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=3,
          font_thickness=2,
          text_color=(0, 255, 0),
          text_color_bg=(0, 0, 0)
          ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

    return text_size

"""Main loop until 'q' is pressed meaning break"""
while True:
    res,frame = cap.read()
    #frame = cv2.resize(frame, (wCam, hCam))
    if not res:
        # if frame is not read
        break
    frame = cv2.flip(frame, 1)
    rgbFrame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    detect = FaceMesh.process(rgbFrame)

    if detect.multi_face_landmarks:

        #landmarks = faceLandmarks(frame, detect.multi_face_landmarks, False)
        landmarks = detect.multi_face_landmarks[0]

        #mpDraw.draw_landmarks(frame,landmarks)

        mainFunction()


    cTime=time.time()
    if (cTime-pTime) ==0:
        """THIS IS TO TACLE division by 0 error"""
        fps = 0
    else:
        fps=int(1/(cTime-pTime))
    pTime=cTime

    draw_text(frame,f'FPS: {fps}',pos=(20,30),font_scale=1,font_thickness=1)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('q') :
        break
cv2.destroyAllWindows()
cap.release()