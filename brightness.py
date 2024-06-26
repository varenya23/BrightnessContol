# Import required Libraries 
import cv2 
import mediapipe as mp 
from math import hypot 
import screen_brightness_control as sbc 
import numpy as np 

  
# Initialize the Model 
mpHands = mp.solutions.hands 
hands = mpHands.Hands( 
    static_image_mode=False, 
    model_complexity=1, 
    min_detection_confidence=0.75, 
    min_tracking_confidence=0.75, 
    max_num_hands=2) 
Draw = mp.solutions.drawing_utils 
  
# To Start capturing video from webcam 
cap = cv2.VideoCapture(0) 

while True: 

    # Read video frame by frame 
    _, frame = cap.read() 

    # Flip image 
    frame = cv2.flip(frame, 1) 

    # Convert BGR image to RGB image 
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    # Process the RGB image 
    Process = hands.process(frameRGB) 

    landmarkList = [] 

    # if hands are present in image(frame) 
    if Process.multi_hand_landmarks: 

        # detect handmarks 
        for handlm in Process.multi_hand_landmarks: 
            for _id, landmarks in enumerate(handlm.landmark): 

                # store height and width of image 
                height, width, color_channels = frame.shape 

                # calculate and append x, y coordinates of handmarks from image(frame) to lmList 
                x, y = int(landmarks.x*width), int(landmarks.y*height) 
                landmarkList.append([_id, x, y]) 

            # draw Landmarks 
            Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS) 

    # If landmarks list is not empty 
    if landmarkList != []: 

        # store x,y coordinates of (tip of) thumb and index finger
        x_1, y_1 = landmarkList[4][1], landmarkList[4][2] 
        x_2, y_2 = landmarkList[8][1], landmarkList[8][2] 

        # Draw circle on thumb and index finger tip. Draw line from thumb to index finger 
        cv2.circle(frame, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED) 
        cv2.circle(frame, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED) 
        cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3) 

        # calculate square root of the sum of squares of the specified arguments. 
        L = hypot(x_2-x_1, y_2-y_1) 

        # Hand range 15 - 220, Brightness range 0 - 100.  
        b_level = np.interp(L, [15, 220], [0, 100]) 

        # set brightness 
        sbc.set_brightness(int(b_level)) 

    # Display Video. When 'a' is entered, close the program
    cv2.imshow('Image', frame) 
    if cv2.waitKey(1) & 0xff == ord('a'): 
        break