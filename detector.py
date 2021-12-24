import imagezmq
import cv2
import imutils


class Detector:
    def __init__(self, receive_port="55555", send_port="55556"):
        self.firstFrame = None
        self.receive_port = receive_port
        self.send_port = send_port

    def detect(self):
        receiver = imagezmq.ImageHub(open_port='tcp://127.0.0.1:' + self.receive_port, REQ_REP=False)
        sender = imagezmq.ImageSender(connect_to='tcp://*:' + self.send_port, REQ_REP=False)

        while True:
            rectangle_list = []
            msg, frame = receiver.recv_image()
            if "quit" in msg:
                self.quit()
                return False

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if self.firstFrame is None:
                self.firstFrame = gray

            frame_delta = cv2.absdiff(self.firstFrame, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(
                thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            for c in cnts:
                if cv2.contourArea(c) < 500:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                rectangle_list.append(((x, y), (x + w, y + h)))

            sender.send_image(rectangle_list, frame)

    def quit(self):
        pass
