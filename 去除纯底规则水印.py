"""
不足之处
- 只能去一些纯色底上的水印
-  水印必须是规则形状
- 框选水印后，需要按ESC键保存退出
"""

import cv2
import numpy as np

# 记录鼠标点击坐标
click_points = []
temp_img = None

# 定义鼠标回调函数（处理鼠标点击/移动事件）
def mouse_callback(event,x,y,flags,param):
    """
    event: 鼠标事件类型
    x,y: 鼠标点击时在图片上的坐标
    flags: 鼠标状态
    """
    global click_points, temp_img

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(click_points) >= 2:
            click_points = [] # 选择大于2时，清空列表
            temp_img = param.copy() # 选择大于2时，重置矩形

        click_points.append((x,y))
        print(f"Chose points yet: {click_points[-1]}") # 方便用户确认选择的点

        if len(click_points) == 2:
            x1, y1 = click_points[0]
            x2, y2 = click_points[1]

            cv2.rectangle(temp_img,(x1,y1),(x2,y2),(0,0,255),1) # 画出矩形（红色）

    elif event == cv2.EVENT_MOUSEMOVE and len(click_points) == 1:
        temp_img = param.copy() # 每次移动都重置图片副本（矩形）
        x1,y1 = click_points[0]
        cv2.rectangle(temp_img,(x1,y1),(x,y),(0,255,0),1) # 绿色预览线

def remove_watermark_with_manual_mark(image_path):
    global temp_img
    img = cv2.imread(image_path)

    temp_img = img.copy()

    # 创建可调整大小的窗口
    cv2.namedWindow("Manually mark the watermark area",cv2.WINDOW_NORMAL)
    # 绑定鼠标回调函数：窗口名、回调函数、给回调函数传的额外参数
    cv2.setMouseCallback("Manually mark the watermark area",mouse_callback,img)

    while True:
        cv2.imshow("Manually mark the watermark area",temp_img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
    
    if len(click_points) != 2:
        print("Error: Need 2 points to locate the watermark.")
        cv2.destroyAllWindows()
        return
    
    (x1,y1),(x2,y2) = click_points

    x1,x2 = min(x1,x2),max(x1,x2)
    y1,y2 = min(y1,y2),max(y1,y2)
    print(f"\nThe last location: \n({x1},{y1}),({x2},{y2})")

    mask = np.zeros(img.shape[:2],dtype=np.uint8)
    mask[y1:y2,x1:x2] = 255

    print("Please wait.")
    repaired_img = cv2.inpaint(img,mask,1,cv2.INPAINT_NS)

    print("Mission accomplished!")
    save_path = "repaired_image.jpg"
    cv2.imwrite(save_path,repaired_img)
    print(f"Saved in the current location.")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("1. Click the upper left corner area of watermark;")
    print("2. Click the lower right corner area of watermark;")
    print("3. Press ESC to finish.")
    print("Please input your address of image:")
    IMAGE_PATH = input()
    remove_watermark_with_manual_mark(IMAGE_PATH)
