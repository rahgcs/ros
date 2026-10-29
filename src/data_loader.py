
import numpy as np
import open3d as o3d

from src.config import DATA_PATH, FRAME_STEP, DEPTH_SCALE, MAX_DEPTH


def get_frames():
    rgb = np.loadtxt(DATA_PATH / "rgb.txt", dtype=str)
    depth = np.loadtxt(DATA_PATH / "depth.txt", dtype=str)

    depth_times = depth[:, 0].astype(float)
    frames = []

    for timestamp, rgb_path in rgb[::FRAME_STEP]:
        timestamp = float(timestamp)

        index = np.argmin(np.abs(depth_times - timestamp))

        if abs(depth_times[index] - timestamp) < 0.02:
            frames.append((rgb_path, depth[index, 1]))

    return frames


def load_rgbd(rgb_path, depth_path, grayscale=False):
    color = o3d.io.read_image(str(DATA_PATH / rgb_path))
    depth = o3d.io.read_image(str(DATA_PATH / depth_path))

    return o3d.geometry.RGBDImage.create_from_color_and_depth(
        color,
        depth,
        depth_scale=DEPTH_SCALE,
        depth_trunc=MAX_DEPTH,
        convert_rgb_to_intensity=grayscale
    )
