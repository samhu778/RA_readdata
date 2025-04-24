
import os
import time
import tqdm
import h5py
import socket

import cv2
os.sys.path.append("/home/developer/aloha-fudan/dateset_prepare/sdk/linux_x64")
import numpy as np

import gene_sdk_module

# from kivcam.kivcam.kivcam import get_image, init_cam, release_cam
from sdk.linux_x64.dataPickingTest import get_pos, get_vel

def get_pos_2(gene_handle):
    left_pos, right_pos = get_pos(gene_handle)
    left_pos = list(left_pos["rax"])
    right_pos = list(right_pos["rax"])
    pos = left_pos + right_pos
    return pos # 7*2=14向量

def capture_one_episode(max_timesteps, dataset_dir, dataset_name):
    """
    For each timestep:
    observations
    - images
        - cam_high          (480, 640, 3) 'uint8'
        - cam_low           (480, 640, 3) 'uint8'
        - cam_left_wrist    (480, 640, 3) 'uint8'
        - cam_right_wrist   (480, 640, 3) 'uint8'
    - qpos                  (14,)         'float64'
    - qvel                  (14,)         'float64'

    action                  (14,)         'float64'
    """
    print(f'----------{dataset_name}, start----------------')
    if not os.path.isdir(dataset_dir):
        os.makedirs(dataset_dir)
    dataset_path = os.path.join(dataset_dir, dataset_name)

    data_dict = {
        '/observations/qpos': [],
        '/observations/qvel': [],
        '/action': [],
    }

    camera_names = ['cam_high', 'cam_low', 'cam_left_wrist', 'cam_right_wrist']
    for cam_name in camera_names:
        data_dict[f'/observations/images/{cam_name}'] = []

    FPS = 50
    DT = 1 / FPS

    for t in range(max_timesteps):
        t0 = time.time() #
        pos = get_pos_2(gene_handle)
        data_dict['/observations/qpos'].append(pos)
        data_dict['/observations/qvel'].append(pos) # 由于现在获取不到速度,暂时用getpos代替getvel
        data_dict['/action'].append(pos) # 由于遥操作没有实现,暂时用getpos代替getaction
    
        for index, cam_name in enumerate(camera_names):
            data_dict[f'/observations/images/{cam_name}'].append(np.random.rand(480,640,3))

            time.sleep(max(0, DT - (time.time() - t0)))

    # HDF5
    t0 = time.time()

    with h5py.File(dataset_path + '.hdf5', 'w', rdcc_nbytes=1024**2*2) as root:
        root.attrs['sim'] = False
        obs = root.create_group('observations')
        image = obs.create_group('images')
        for cam_name in camera_names:
                _ = image.create_dataset(cam_name, (max_timesteps, 480, 640, 3), dtype='uint8',
                                         chunks=(1, 480, 640, 3), )
        _ = obs.create_dataset('qpos', (max_timesteps, 14))
        _ = obs.create_dataset('qvel', (max_timesteps, 14))
        _ = root.create_dataset('action', (max_timesteps, 14))

        for name, array in data_dict.items():
            root[name][...] = array

    print(f'Saving: {time.time() - t0:.1f} secs')
    print(f'{dataset_name}, end')

    return True


if __name__ == '__main__':
    max_timesteps = 240
    dataset_dir = './test_record_data'

    # init cameras and arms
    # init_cam()
    gene_handle = gene_sdk_module.ConnectRobotController("192.168.89.125")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = ''
        port = 8887
        s.bind((host, port))

        s.listen()
        print("Server is listening on", (host, port))

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            for i in range(50):

                flag_start = 'start'
                conn.sendall(flag_start.encode())

                dataset_name = 'episod_' + str(i)
                capture_one_episode(max_timesteps, dataset_dir, dataset_name)

                flag_end  = conn.recv(1024)
                if flag_end:
                    continue

    # release_cam()