
from pathlib import Path
import open3d as o3d

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "rgbd_dataset_freiburg1_room"
OUTPUT_PATH = BASE_DIR / "outputs"

FRAME_STEP = 2
VOXEL_SIZE = 0.01
MAX_DEPTH = 3.5
DEPTH_SCALE = 5000.0

WIDTH, HEIGHT = 640, 480
FX, FY = 525.0, 525.0
CX, CY = 319.5, 239.5

INTRINSIC = o3d.camera.PinholeCameraIntrinsic(
    WIDTH, HEIGHT, FX, FY, CX, CY
)

MAX_JUMP = 0.25

OUTPUT_PATH.mkdir(exist_ok=True)
