import cv2
from threading import Thread

class AcpTrafego(Thread):
    def __init__(self, thread_id, name, filename='traffic1.avi', reference_frame=None, image_area=None):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.filename = filename
        self.reference_frame = reference_frame
        self.image_area = image_area
        self.cap = cv2.VideoCapture(filename)

    def run(self):
        self.do_monitoring()

    def do_monitoring(self):

        while True:
            ret, frame = self.cap.read()

            if ret is False:
                break
            else:
                if self.reference_frame is None:
                    self.reference_frame = frame
                    self.reference_frame = cv2.cvtColor(self.reference_frame, cv2.COLOR_BGR2GRAY)
                    self.image_area = self.reference_frame.shape[0] * self.reference_frame.shape[1]
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                difference = cv2.absdiff(self.reference_frame, gray)
                blur = cv2.medianBlur(difference, 31)

                f, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                (_, contours, _) = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for i in contours:
                    contour_area = cv2.contourArea(i)
                    if (contour_area > 0.001*self.image_area)and(contour_area < 0.03 * self.image_area):
                        (x, y, w, h) = cv2.boundingRect(i)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

                cv2.imshow("frames", frame)
                if cv2.waitKey(1) == ord('q'):
                    break
