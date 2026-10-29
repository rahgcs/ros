
# import open3d as o3d
# import numpy as np
# import imageio.v2 as imageio

# ply_path = "room_mesh.ply"
# output_gif = "room_3d.gif"

# # Load point cloud or mesh
# geometry = o3d.io.read_point_cloud(ply_path)

# if geometry.is_empty():
#     geometry = o3d.io.read_triangle_mesh(ply_path)

# vis = o3d.visualization.Visualizer()
# vis.create_window(visible=True, width=800, height=600)
# vis.add_geometry(geometry)

# # Set camera view
# view = vis.get_view_control()
# view.set_zoom(0.7)

# frames = []

# for i in range(120):
#     vis.poll_events()
#     vis.update_renderer()

#     # Capture rendered frame
#     frame = np.asarray(vis.capture_screen_float_buffer(do_render=True))
#     frame = (frame * 255).astype(np.uint8)
#     frames.append(frame)

#     # Rotate camera
#     view.rotate(6, 0)

# vis.destroy_window()

# # Save GIF
# imageio.mimsave(output_gif, frames, fps=20, loop=0)

# print(f"GIF saved: {output_gif}")


import open3d as o3d
import numpy as np
import imageio.v2 as imageio

ply_path = "output/room_mesh.ply"
output_gif = "room_180.gif"

# Load PLY
pcd = o3d.io.read_point_cloud(ply_path)

# 1. Flip vertically (180 degrees around X-axis)
center = pcd.get_center()

R_flip = pcd.get_rotation_matrix_from_xyz((np.pi, 0, 0))
pcd.rotate(R_flip, center=center)

# 2. Visualizer
vis = o3d.visualization.Visualizer()
vis.create_window(width=800, height=600, visible=True)
vis.add_geometry(pcd)

view = vis.get_view_control()
view.set_zoom(0.7)

frames = []

# 3. Full 360-degree rotation
total_frames = 120
rotation_per_frame = 180 / total_frames

for i in range(total_frames):

    # Rotate camera horizontally
    view.rotate(rotation_per_frame * 5, 0)

    vis.poll_events()
    vis.update_renderer()

    frame = np.asarray(
        vis.capture_screen_float_buffer(do_render=True)
    )

    frame = (frame * 255).astype(np.uint8)
    frames.append(frame)

vis.destroy_window()

# 4. Save GIF
imageio.mimsave(
    output_gif,
    frames,
    fps=20,
    loop=0
)

print("GIF generated:", output_gif)
