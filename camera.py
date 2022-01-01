import cv2
import time
from datetime import datetime

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS) # (30 fps)
# print(fps)

background = None
frame_count = 0
baby_state = "awake"
state_change = False
awake_start = None
asleep_start = None
total_movement = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if background is None:
        empty_bed = gray
        background = gray
        continue
    
    frame_count += 1
    if frame_count % 30 == 0:
        background = gray

    subtraction = cv2.absdiff(background, gray)

    threshold = cv2.threshold(subtraction, 25, 255, cv2.THRESH_BINARY)[1]

    threshold = cv2.dilate(threshold, None, iterations=2)

    contouring = threshold.copy()

    contours, hierarchy = cv2.findContours(contouring, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(contouring, contours, -1, (100, 0, 255), 2)


    movement_count = 0 # tracking the number of movements above a threshold
    for c in contours:
        if cv2.contourArea(c) < 500:
            continue

        (x ,y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) # draw the box for the movement
        
        movement_count += 1

    now = datetime.now()
    
    if baby_state == "awake": # require 60 contiguous seconds of no movement to be considered asleep
        if movement_count == 0:
            if state_change == False:
                asleep_start = now
                state_change = True
            elif ((now - asleep_start).seconds >= 60):
                baby_state = "asleep"
                state_change = False
                print(f'Asleep at {asleep_start}')
                asleep_start = None
        else:
            state_change = False
            asleep_start = None
    else:
        if (movement_count != 0) and (frame_count % 30 == 9): # this is a hack
            total_movement += 1 # acknowledge movement
            if state_change == False: # if he is current in the sleep state, then set him to pending wakeup
                awake_start = now
                state_change = True
        
        
        if (awake_start is not None) and ((now - awake_start).seconds >= 60): # check if 60 seconds have elapsed
            state_change = False
            # print(f'Total Movement: {total_movement} at {now}')
            if total_movement >= 20: # check if he moved 20 times in those 60 seconds
                baby_state = "awake"
                print(f'Awake at {awake_start}')
            total_movement = 0
            awake_start = None
            
    
    cv2.putText(frame, now.strftime("%H:%M:%S"), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)
    # cv2.putText(frame, f'Asleep MPM: {total_movement}', (200,30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)
    cv2.putText(frame, f'{baby_state}', (500,30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)

    cv2.imshow("Camera", frame)
    # cv2.imshow("Threshold", threshold)
    # cv2.imshow("Subtraction", subtraction)
    # cv2.imshow("Contour", contouring)

    key = cv2.waitKey(1) & 0xFF
    time.sleep(0.015)
    if key == ord("q") or key == 27:
        break

cap.release()
cv2.destroyAllWindows()