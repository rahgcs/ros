
import open3d as o3d
from src.config import OUTPUT_PATH


def show_point_cloud():
    cloud = o3d.io.read_point_cloud(
        str(OUTPUT_PATH / "room_fused.ply")
    )

    o3d.visualization.draw_geometries(
        [cloud],
        window_name="Fused Point Cloud"
    )


def show_mesh(mesh):
    o3d.visualization.draw_geometries(
        [mesh],
        window_name="3D Room Reconstruction",
        mesh_show_back_face=True,
        mesh_show_wireframe=False
    )