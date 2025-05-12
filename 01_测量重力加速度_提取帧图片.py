import cv2
import os
cap = cv2.VideoCapture("freefallby60f.mp4")  # 打开自由落体视频
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()                 # 逐帧提取并保存图片
    if not ret:
        break
    cv2.imwrite("extframes_"+str(frame_count)+".jpg", frame)
    frame_count += 1
cap.release()                               # 释放资源