#-*- coding:utf-8 -*-

from PyQt5 import uic 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyautogui

import cv2
import glob
import sys, os

import traceback
import warnings
warnings.filterwarnings( 'ignore' )

from utils.convert import *

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('4CamViewer.ui')
form_class = uic.loadUiType(form)[0]

class MyApp(QWidget, form_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.vars = locals()
        self.initUI()


    def initUI(self):
        # 카메라 셋팅
        cams = self.search_cam()
        print(cams)
        self.vcap0 = cv2.VideoCapture(cams[0])
        self.vcap1 = cv2.VideoCapture(cams[1])
        self.vcap2 = cv2.VideoCapture(cams[2])
        self.vcap3 = cv2.VideoCapture(cams[3])

        # 영상 전달
        self.send_video_frame()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.showMaximized()

        self.start_run()
        
        
    def start_run(self):
        self.timer = QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.send_video_frame)
                   

    def send_video_frame(self):
        im0, im1, im2, im3 = open_vcap(self.vcap0, self.vcap1, self.vcap2, self.vcap3)
        self.img = concat_img(im0, im1, im2, im3)
        self.qimg = QImage(self.img, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        self.pix = QPixmap.fromImage(self.qimg)
        self.video_frame.setPixmap(self.pix)
        self.video_frame.setScaledContents(True)


    def search_cam(self):
        cams = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cams.append(i)
        if len(cams) >= 5:
            cams = cams[1:]
        elif len(cams) == 3:
            cams.append(3)
        elif len(cams) == 2:
            cams.append(3)
            cams.append(2)
        elif len(cams) == 1:
            cams.append(3)
            cams.append(2)
            cams.append(1)
        return cams


    def mouseDoubleClickEvent(self, event) -> None: 
        if event.buttons() & Qt.LeftButton:
            pyautogui.hotkey('win', 'alt', 'r')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())