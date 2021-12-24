import cv2
import imagezmq

class Streamer:
    def __init__(self, video_path,send_port="55555"):
        self.video_path = video_path
        self.send_port = send_port

    def validate_video_path(self):
        self.video_capture = cv2.VideoCapture(self.video_path)
        return self.video_capture.isOpened()

    def stream(self):
        if not self.validate_video_path():
            return False
        sender = imagezmq.ImageSender(connect_to='tcp://*:55555', REQ_REP=False)

        # frames per second!!!!!!!!!!!!!!!!!!!!!

        while True:
            flag, frame = self.video_capture.read()

            if not flag:
                self.quit()
                break

            sender.send_image("", frame)

    def quit(self):
        pass

if __name__ == '__main__':
    streamer = Streamer("C:/Users/Paz/Desktop/AxonVision/source/People - 6387 (2).mp4")
    streamer.stream()