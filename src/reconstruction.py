
import numpy as np
import open3d as o3d
import open3d.core as o3c

from .config import (
    DATA_PATH, OUTPUT_PATH, INTRINSIC,
    VOXEL_SIZE, DEPTH_SCALE, MAX_DEPTH
)
from .data_loader import load_rgbd


# 1. Create fused point cloud

def create_point_cloud(frames, poses):
    combined = o3d.geometry.PointCloud()

    for i, ((rgb_path, depth_path), pose) in enumerate(zip(frames, poses)):
        rgbd = load_rgbd(rgb_path, depth_path)

        cloud = o3d.geometry.PointCloud.create_from_rgbd_image(
            rgbd, INTRINSIC, np.linalg.inv(pose)
        )

        combined += cloud.voxel_down_sample(VOXEL_SIZE * 2)

        if i % 25 == 0:
            combined = combined.voxel_down_sample(VOXEL_SIZE * 2)

    combined = combined.voxel_down_sample(VOXEL_SIZE * 2)

    o3d.io.write_point_cloud(
        str(OUTPUT_PATH / "room_fused.ply"), combined
    )

    return combined


# 2. Reconstruct mesh using Tensor TSDF

def create_mesh(frames, poses):
    device = o3c.Device("CPU:0")

    volume = o3d.t.geometry.VoxelBlockGrid(
        attr_names=("tsdf", "weight", "color"),
        attr_dtypes=(o3c.float32, o3c.float32, o3c.float32),
        attr_channels=((1,), (1,), (3,)),
        voxel_size=VOXEL_SIZE,
        block_resolution=16,
        block_count=100000,
        device=device
    )

    K = o3c.Tensor(INTRINSIC.intrinsic_matrix, o3c.float64)

    for (rgb_path, depth_path), pose in zip(frames, poses):
        depth = o3d.t.io.read_image(
            str(DATA_PATH / depth_path)
        ).to(device)

        color = o3d.t.io.read_image(
            str(DATA_PATH / rgb_path)
        ).to(device)

        extrinsic = o3c.Tensor(
            np.linalg.inv(pose), o3c.float64
        )

        blocks = volume.compute_unique_block_coordinates(
            depth, K, extrinsic, DEPTH_SCALE, MAX_DEPTH
        )

        volume.integrate(
            blocks, depth, color, K, extrinsic,
            DEPTH_SCALE, MAX_DEPTH
        )

    mesh = volume.extract_triangle_mesh().to_legacy()

    if mesh.is_empty():
        raise RuntimeError("Tensor TSDF produced an empty mesh.")

    mesh.compute_vertex_normals()

    o3d.io.write_triangle_mesh(
        str(OUTPUT_PATH / "room_mesh.ply"), mesh
    )

    return mesh
