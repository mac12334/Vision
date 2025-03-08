import numpy as np
import cv2
import glob

# Path to your 50 checkerboard images
image_path = "./images/*.png"

# Checkerboard properties (7x7 INNER corners, since an 8x8 board has 7 intersections)
CHECKERBOARD = (7, 7)
square_size = 0.025  # Adjust if each square is not 2.5cm (25mm)

# Prepare 3D object points
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= square_size  # Scale by square size

# Arrays to store 3D points (real-world) and 2D points (image plane)
objpoints = []
imgpoints = []

# Load images
images = glob.glob(image_path)
if not images:
    print("❌ No images found! Check the path.")
    exit()

print(f"📸 Found {len(images)} images. Starting calibration...")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find the checkerboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)
        cv2.imshow("Checkerboard Detection", img)
        cv2.waitKey(100)
    else:
        print(f"⚠️ Checkerboard not detected in {fname}")

cv2.destroyAllWindows()

# Perform camera calibration
if len(objpoints) > 0:
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )
    np.savez("calibration_data.npz", camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
    print("\n✅ Camera Calibration Successful!")
    print("📸 Camera Matrix:\n", camera_matrix)
    print("📏 Distortion Coefficients:\n", dist_coeffs)
else:
    print("\n❌ Calibration failed. No valid checkerboard detections found.")

#run “python3 calibrate_camera.py”
