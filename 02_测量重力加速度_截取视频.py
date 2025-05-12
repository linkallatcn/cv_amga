import cv2
cap = cv2.VideoCapture("freefallby60f.mp4")      #打开拍摄完成的自由落体视频
fps = cap.get(cv2.CAP_PROP_FPS)                  #获取自由落体视频帧率
fourcc = cv2.VideoWriter_fourcc(*'mp4v')         # 视频编码器
out = cv2.VideoWriter("freefallby60f_capture.mp4", fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
cap.set(cv2.CAP_PROP_POS_FRAMES, 25)             #跳转到指定帧
for frame_num in range(start_frame, end_frame):  # 读取并写入视频片段
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
cap.release()                                    # 释放资源
out.release()                                    # 释放资源
