import cv2
import imagezmq


class Streamer:
    def __init__(self, video_path, send_port="55555"):
        self.video_path = video_path
        self.send_port = send_port

    def stream(self):
        video_capture = cv2.VideoCapture(self.video_path)

        if not video_capture.isOpened():
            self.quit()
            return False

        sender = imagezmq.ImageSender(connect_to='tcp://*:' + self.send_port, REQ_REP=False)

        while True:
            flag, frame = video_capture.read()

            if not flag:
                self.quit()
                return False

            sender.send_image("", frame)

    def quit(self):
        pass
