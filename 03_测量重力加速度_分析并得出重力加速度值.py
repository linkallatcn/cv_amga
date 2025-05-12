import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import matplotlib as mpl
mpl.rcParams["font.family"] = "FangSong"  # 设置全局字体为仿宋
mpl.rcParams["axes.unicode_minus"] = False  # 确保负号显示正常

# 加载视频
#video_path = "free_fall_video_60fps.mp4"
video_path = "free_fall_video_60fps_out_25_41.mp4"
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功加载
if not cap.isOpened():
    print("无法打开视频文件！")
    exit()

# 获取视频的帧率
fps = cap.get(cv2.CAP_PROP_FPS)
print("fps:", fps)

# 初始化变量
positions = []  # 存储物体的垂直位置
times = []      # 存储时间

# 目标检测和跟踪
c=24
while cap.isOpened():
    c+=1
    ret, frame = cap.read()
    if not ret:
        break

    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用阈值分割检测物体
    
    _, binary = cv2.threshold(gray, 90+(c-24)*3, 150, cv2.THRESH_BINARY)  # 调整阈值 #170, 180 #25:33使用100,150

    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # 调整轮廓检测方法

    # 假设最大的轮廓是自由落体的物体
    if len(contours) > 0:
        for i in contours:
            #print(c,"cv2.boundingRect(i):",cv2.boundingRect(i))
            (x, y, w, h) = cv2.boundingRect(i)
            if 480<x<550 and 1000<w*h<40000:
                suitable_contour = i
                positions.append(y)
                times.append(len(times) / fps)  # 记录时间
                print(c,f"检测到物体：位置 ({x}, {y}), 大小 ({w}, {h})")
        

        # 记录物体的垂直位置（y坐标）
        

        # 在图像上绘制轮廓
        cv2.drawContours(frame, [suitable_contour], -1, (0, 255, 0), 2)

        # 调试信息
        
    else:
        print("未检测到物体！")  # 调试信息

    # 显示帧
    # 获取屏幕分辨率
    screen_width = 1920  # 替换为你的屏幕宽度
    screen_height = 1080  # 替换为你的屏幕高度

    # 获取图像尺寸
    image_height, image_width = frame.shape[:2]

    # 计算缩放比例
    scale = min(screen_width / image_width, screen_height / image_height)

    # 缩放图像
    resized_image = cv2.resize(frame, (int(image_width * scale), int(image_height * scale)))
    cv2.imshow("Frame", resized_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()

# 检查是否有数据
if len(positions) == 0:
    print("未检测到物体，无法拟合数据！")
    exit()

# 转换为数组
positions = np.array(positions)
times = np.array(times)
print("positions:",positions)
print("times:",times)
# 定义自由落体运动方程
def free_fall_equation(t, g, y0, v0):
    return y0 + v0 * t + 0.5 * g * t**2

# 使用SciPy拟合数据
# 比例尺：假设 4000 像素 = 1 米
scale = 0.1/420  # 单位：m/像素   #0.000375  #0.0003  #0.1/420 0.00025
# 将像素转换为米
positions_meters = positions * scale

popt, _ = curve_fit(free_fall_equation, times, positions)
popt_meters, _ = curve_fit(free_fall_equation, times, positions_meters)

# 提取拟合参数
g_fitted = popt_meters[0]  # 拟合的重力加速度
#y0_fitted = popt_meters[1]  # 初始位置
#v0_fitted = popt_meters[2]  # 初始速度

# 输出结果
print(f"拟合的重力加速度: {g_fitted:.2f} m/s²")

# 绘制拟合曲线
plt.scatter(times, positions_meters, label="实际数据")
plt.plot(times, free_fall_equation(times, *popt_meters), color='red', label="拟合曲线")
plt.xlabel("时间 (s)")
plt.ylabel("垂直位置 (米)")
plt.title(f'自由落体重力加速度拟合结果: $g = {g_fitted:.3f} \, \mathrm{{m/s^2}}$')
plt.legend()
plt.show()