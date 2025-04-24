
import os
import time
import h5py
import socket

os.sys.path.append("/home/developer/aloha-fudan/dateset_prepare/sdk/linux_x64")
import gene_sdk_module

from sdk.linux_x64.dataPickingTest import get_pos

from get_image import initialize_cameras, release_cameras, capture_camera_image

def get_pos_2(gene_handle):
    left_pos, right_pos = get_pos(gene_handle)
    left_pos = list(left_pos["rax"])
    right_pos = list(right_pos["rax"])
    pos = left_pos + right_pos
    return pos # 7*2=14向量

def capture_one_episode(max_timesteps, dataset_dir, dataset_name, camera_list):
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

    # creating dataset dir and path
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
    t1 = time.time() #
    for t in range(max_timesteps):
        t0 = time.time() #
        pos = get_pos_2(gene_handle)
        data_dict['/observations/qpos'].append(pos)
        data_dict['/observations/qvel'].append(pos) # 由于现在获取不到速度,暂时用getpos代替getvel
        data_dict['/action'].append(pos) # 由于遥操作没有实现,暂时用getpos代替getaction
    
        for index, cam_name in enumerate(camera_names):
            image = capture_camera_image(camera_list[index])
            data_dict[f'/observations/images/{cam_name}'].append(image)

        time.sleep(max(0, DT - (time.time() - t0))) # control frequency

    t2 = time.time() #
    print(f'collect {max_timesteps} steps data, consume time {t2 - t1}s')
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
    dataset_dir = './random_line/end_pose'
    max_timesteps = 600

    # init cameras and arms
    camera_names = [6,8,4,2] # corresponding to ['cam_high', 'cam_low', 'cam_left_wrist', 'cam_right_wrist']
    width = 640
    height = 480
    camera_list = initialize_cameras(camera_names, width, height)

    gene_handle = gene_sdk_module.ConnectRobotController("192.168.89.125")

    # start communciton
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = ''
        port = 8887
        s.bind((host, port))

        s.listen()
        print("Server is listening on", (host, port))

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            flag_start = 'start'
            conn.sendall(flag_start.encode())

            dataset_name = 'episode_64'
            capture_one_episode(max_timesteps, dataset_dir, dataset_name, camera_list)

            release_cameras(camera_list)
