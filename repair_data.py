import os

import h5py
import argparse


import IPython
e = IPython.embed

JOINT_NAMES = ["waist", "shoulder", "elbow", "forearm_roll", "wrist_angle", "wrist_rotate"]
STATE_NAMES = JOINT_NAMES + ["gripper"]

def load_hdf5(dataset_dir, dataset_name):
    dataset_path = os.path.join(dataset_dir, dataset_name + '.hdf5')
    if not os.path.isfile(dataset_path):
        print(f'Dataset does not exist at \n{dataset_path}\n')
        exit()

    with h5py.File(dataset_path, 'r') as root:
        is_sim = root.attrs['sim']
        qpos = root['/observations/qpos'][()]
        qvel = root['/observations/qvel'][()]
        action = root['/action'][()]
        image_dict = dict()
        for cam_name in root[f'/observations/images/'].keys():
            image_dict[f'/observations/images/{cam_name}'] = root[f'/observations/images/{cam_name}'][()]

    return qpos, qvel, action, image_dict

def main(args):
    dataset_dir = args['dataset_dir']
    
    for i in [14]:
        if i == 0:
            continue
        episode_idx = i
        dataset_name = f'episode_{episode_idx}'
        qpos, qvel, action, image_dict = load_hdf5(dataset_dir, dataset_name)

        dataset_path = os.path.join(dataset_dir, dataset_name)

        with h5py.File(dataset_path + '.hdf5', 'r+', rdcc_nbytes=1024**2*2) as root:
            for name, array in image_dict.items():
                if name == '/observations/images/cam_high':
                    root['/observations/images/cam_left_wrist'][...] = array

                elif name == '/observations/images/cam_low':
                    root['/observations/images/cam_right_wrist'][...] = array

                elif name == '/observations/images/cam_left_wrist':
                    root['/observations/images/cam_high'][...] = array

                elif name == '/observations/images/cam_right_wrist':
                    root['/observations/images/cam_low'][...] = array


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_dir', default='/home/developer/aloha-fudan/dateset_prepare/broken_line', type=str, help='Dataset dir.')
    main(vars(parser.parse_args()))

