import cv2
import time
from datetime import datetime

class CameraClass(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) # (30 fps)

        self.background = None
        self.empty_bed = None
        self.frame_count = 0
        self.baby_state = "awake"
        self.state_change = False
        self.awake_start = None
        self.asleep_start = None
        self.total_movement = 0
        self.movement_count = 0

    def get_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.background is None: # initial background capture
            self.empty_bed = gray
            self.background = gray

        self.frame_count += 1
        if self.frame_count % 30 == 0:
            self.background = gray

        subtraction = cv2.absdiff(self.background, gray)

        threshold = cv2.threshold(subtraction, 25, 255, cv2.THRESH_BINARY)[1]

        threshold = cv2.dilate(threshold, None, iterations=2)

        contouring = threshold.copy()

        contours, hierarchy = cv2.findContours(contouring, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(contouring, contours, -1, (100, 0, 255), 2)

        for c in contours:
            if cv2.contourArea(c) < 500:
                continue

            (x ,y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) # draw the box for the movement

            self.movement_count += 1

        now = datetime.now()

        if self.baby_state == "awake": # require 60 contiguous seconds of no movement to be considered asleep
            if self.movement_count == 0:
                if self.state_change == False:
                    self.asleep_start = now
                    self.state_change = True
                elif ((now - self.asleep_start).seconds >= 60):
                    self.baby_state = "asleep"
                    self.state_change = False
                    print(f'Asleep at {self.asleep_start}')
                    self.asleep_start = None
            else:
                self.state_change = False
                self.asleep_start = None
        else:
            if (self.movement_count != 0) and (self.frame_count % 30 == 9): # this is a hack
                self.total_movement += 1 # acknowledge movement
                if self.state_change == False: # if he is current in the sleep state, then set him to pending wakeup
                    self.awake_start = now
                    self.state_change = True


            if (self.awake_start is not None) and ((now - self.awake_start).seconds >= 60): # check if 60 seconds have elapsed
                self.state_change = False
                # print(f'Total Movement: {self.total_movement} at {now}')
                if self.total_movement >= 20: # check if he moved 20 times in those 60 seconds
                    baby_state = "awake"
                    print(f'Awake at {self.awake_start}')
                self.total_movement = 0
                self.awake_start = None


        # cv2.putText(frame, now.strftime("%H:%M:%S"), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)
        # cv2.putText(frame, f'Asleep MPM: {total_movement}', (200,30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)
        # cv2.putText(frame, f'{self.baby_state}', (500,30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)

        return frame



        # cv2.imshow("Camera", frame)
        # cv2.imshow("Threshold", threshold)
        # cv2.imshow("Subtraction", subtraction)
        # cv2.imshow("Contour", contouring)

    #     key = cv2.waitKey(1) & 0xFF
    #     time.sleep(0.015)
    #     if key == ord("q") or key == 27:
    #         break
    #
    # cap.release()
    # cv2.destroyAllWindows()