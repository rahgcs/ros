
import numpy as np
import open3d as o3d

from .config import INTRINSIC, OUTPUT_PATH, MAX_JUMP
from .data_loader import load_rgbd


def estimate_poses(frames):
    poses = [np.eye(4)]

    option = o3d.pipelines.odometry.OdometryOption()
    jacobian = o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm()

    previous = load_rgbd(*frames[0], grayscale=True)
    last_rel = np.eye(4)

    for rgb_path, depth_path in frames[1:]:
        current = load_rgbd(rgb_path, depth_path, grayscale=True)

        success, transform, _ = o3d.pipelines.odometry.compute_rgbd_odometry(
            current,
            previous,
            INTRINSIC,
            last_rel,
            jacobian,
            option
        )

        if success and np.linalg.norm(transform[:3, 3]) < MAX_JUMP:
            last_rel = transform
        else:
            transform = last_rel

        poses.append(poses[-1] @ transform)
        previous = current

    poses = np.array(poses)
    np.save(OUTPUT_PATH / "camera_poses.npy", poses)

    return poses
