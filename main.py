
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.data_loader import get_frames
from src.odometry import estimate_poses
from src.reconstruction import create_point_cloud, create_mesh
from src.visualize import show_point_cloud, show_mesh


def main():
    # 1. Load RGB-D frames
    frames = get_frames()

    if not frames:
        raise ValueError("No RGB-D frames found.")

    print("Frames:", len(frames))

    # 2. Estimate camera poses
    poses = estimate_poses(frames)
    print("Camera poses calculated.")

    # 3. Create fused point cloud
    cloud = create_point_cloud(frames, poses)
    print("Point cloud:", len(cloud.points), "points")
    show_point_cloud()

    # 4. Reconstruct 3D mesh using Tensor TSDF
    mesh = create_mesh(frames, poses)

    print("Mesh vertices:", len(mesh.vertices))
    print("Mesh triangles:", len(mesh.triangles))

    show_mesh(mesh)


if __name__ == "__main__":
    main()
