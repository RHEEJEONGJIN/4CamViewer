import cv2
import numpy as np

def open_vcap(vcap0, vcap1, vcap2, vcap3):
    black_screen = np.zeros((192, 256, 3), np.uint8)
    if not (vcap0.isOpened()):
        im0 = black_screen
    else:
        _, im0 = vcap0.read()
    if not (vcap1.isOpened()):
        im1 = black_screen
    else:
        _, im1 = vcap1.read()
    if not (vcap2.isOpened()):
        im2 = black_screen
    else:
        _, im2 = vcap2.read()
    if not (vcap3.isOpened()):
        im3 = black_screen
    else:
        _, im3 = vcap3.read()
    return im0, im1, im2, im3


def concat_img(im0, im1, im2, im3):  
    im01 = cv2.hconcat([im0, im1])
    im23 = cv2.hconcat([im2, im3])
    img = cv2.vconcat([im01, im23]) 
    return img