import cv2
import time

# ceshi摄像头
def test_camera(camera_name):
    cap = cv2.VideoCapture(camera_name)

    if cap.isOpened():
        ret, frame = cap.read()
        cv2.imwrite(f"{camera_name}.png", frame)
        cap.release()
    else:
        print(f'no camer {camera_name}')


# 初始化所有摄像头
def initialize_cameras(camera_names, width, height):
    camera_list = []
    for camera_name in camera_names:  # 假设摄像头设备名分别是 video2, video3, video4, video5
        cap = cv2.VideoCapture(camera_name)

        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            cap.set(cv2.CAP_PROP_FPS, 30)
            camera_list.append(cap)
            time.sleep(2)
        else:
            print(f"Error: Unable to open camera {camera_name}.")
    return camera_list

# 捕获指定摄像头的当前图片
def capture_camera_image(camera):
    # 捕获图像
    ret, frame = camera.read()
    if ret:
        return frame
    else:
        print(f'no {camera}')
        return


# 捕获指定摄像头的当前图片
def capture_camera_image_2(camera_name):
    cap = cv2.VideoCapture(camera_name)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if cap.isOpened():
        ret, frame = cap.read()

        if ret:
            # cv2.imwrite(f"{camera_name}.png", frame)
            cap.release()
            return frame
        else:
            print(f'no camer {camera_name}')
    else:
        print(f'no camer {camera_name}')

# 释放所有摄像头
def release_cameras(camera_names):
    for camera in camera_names:
        camera.release()


if __name__ == "__main__":
    test_camera(2)
    test_camera(4)
    test_camera(6)
    test_camera(8)
    print('done')

    #########################################

    # width = 640
    # height = 480
    # camera_list = initialize_cameras(width, height)

    # max_timesteps = 800
    # t1 = time.time()
    # for index in range(max_timesteps):
    #     for camera in camera_list:
    #         capture_camera_image(camera)

    # t2 = time.time()
    # print(t2 - t1)

    # release_cameras(camera_list)
    # print('done')
    #############################################
    # camera_names = [3,7,10,12]
    # camera_names = [2,4,6,8]
    # for camera_name in camera_names:
    #     capture_camera_image_2(camera_name)

    # print('done')
    #############################################

    # FPS = 50
    # DT = 1 / FPS
    # max_timesteps = 800

    # data_dict = {
    #     '/observations/qpos': [],
    #     '/observations/qvel': [],
    #     '/action': [],
    # }

    # width = 640
    # height = 480
    # camera_names = [2, 4, 6, 8]
    # camera_list = initialize_cameras(camera_names, width, height)


    # for cam_name in camera_list:
    #     data_dict[f'/observations/images/{cam_name}'] = []

    # t0 = time.time() #

    # for t in range(max_timesteps):

    #     for index, cam_name in enumerate(camera_list):

    #         colored_image = capture_camera_image(cam_name)
    #         # cv2.imwrite(f"test_image/{t}_{cam_name}.png", colored_image)
    #         data_dict[f'/observations/images/{cam_name}'].append(colored_image)
    #         # time.sleep(max(0, DT - (time.time() - t0)))

    # t1  = time.time()
    # print(f'cost {t1 - t0}')

    # release_cameras(camera_list)

    # print('done')