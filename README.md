Module is devided into two parts:
---

These are core geometrical approaches to solve the problem without using external deep model.

***odometry algorithm:***
 It estimated the camera postions accross the frames. Calcuate the geometrical and spatial(contrast) difference from previous frames.





***reconstruction :*** 
crearing point clouds + TSDF

Creating point clouds: tranform RGB info + depth into the 3D points ---> transform these point into 3d world coordinates ---> Fusion(combined accross the frames)

Worked on Open Source data similer to AR Core. 
https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros_ws.pdf



AR Core data/
- RGB
- Depth Maps
- Poses(Rotation)
- Translation (words coordinates)
- Camera Intrinsics
- Time stamps





```json   

Input Smaple

 "intrinsics": {
    "width": 640,
    "height": 480,
    "fx": 525.0,
    "fy": 525.0,
    "cx": 319.5,
    "cy": 239.5
  },
  "frames": [
    {
      "color": "frames/0000-color.png",
      "depth": "frames/0000-depth.raw",
      "camera_pose": [
        [
          0.6417163755552173,
          0.5200234776992612,
          -0.563715953283071,
          -0.8683
        ],
        [
          -0.7662444835312714,
          0.40337702302857376,
          -0.5001563443069585,
          0.6026
        ],
        [
          -0.03270297849081383,
          0.7529027559613337,
          0.6573187622939558,
          1.5627
        ],
        [
          0.0,
          0.0,
          0.0,
          1.0
        ]
      ]
    },
```
---

Camera Trajectory by Odometry:

<img src="assets\camera_trajectory.png">

<img src="assets\Screenshot 2026-10-30 044342.png">

---

**Some Shortcommings:**

results might be more clear and robust:
- This is open source data. Some of parts such as celling has missing in the frmaes. 
- movement of the camera is a bit fast, so the sptiality in the frames changes rapidly. The information is captured by the camera is less.

Created a video file with frame to make the visulization of input:

! [input_video](room_scan_video.mp4)

! [output(3d_reconstructed_plane)](outputs\room_mesh.ply)
