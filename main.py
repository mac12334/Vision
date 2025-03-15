import cv2
import apriltag
import numpy
import math
import socket
import convert_to_dict

cap = cv2.VideoCapture(0)
op = apriltag.DetectorOptions("tag36h11")
detect = apriltag.Detector(op)


calib = numpy.load("./calibration_data.npz")
cam_mtx = calib["camera_matrix"]
camera_params = [cam_mtx[0, 0], cam_mtx[1, 1], cam_mtx[0, 2], cam_mtx[1, 2]]

host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host.bind(("0.0.0.0", 9480))
host.listen(1)

apriltagData = convert_to_dict.allInOne("./apriltags.txt")
print(apriltagData)

# client, _ = host.accept()

while True:
   res, frame = cap.read()

   if not res:
       print("failed to load")
       break
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   result = detect.detect(gray)
  
   for r in result:
       arr, _, _ = detect.detection_pose(r, camera_params)
       yaw = math.atan2(arr[1][0], arr[0][0])
       pitch = math.atan2(-arr[2][0], math.sqrt(arr[2][1]**2 + arr[2][2]**2))
       roll = math.atan2(arr[2][1], arr[2][2])

       # the metrics is assuming the apriltag is 1 unit by 1 unit to fix this you need to multiply by the height of the apriltag and divide it by 12

       # roboY you need to inverse x to get the y of the robot, Y is left of the robot
       roboY = int((((arr[0][3] * -1) * 0.15875)) * 1000)
       # roboX you need to use z to get x, basically X is forward
       roboX = int((((arr[2][3]) * 0.15875)) * 1000)
       
       #roboTheta gets the angle from roboY and the nearest apriltag
       roboTheta = int(-(math.degrees(yaw)) * 1000)

       # put the current position to be relative to the field
       apRefPos = apriltagData[r.tag_id]

       actualX = apRefPos[0] - (roboX / 1000)
       actualY = apRefPos[1] - (roboY / 1000)

       print(f"x: {actualX}, Y: {actualY}")
       
    #    client.send(f"{r.tag_id},{roboX},{roboY},{roboTheta}\n".encode("ascii"))

       pa, pb, pc, pd = r.corners
       pa = int(pa[0]), int(pa[1])
       pb = int(pb[0]), int(pb[1])
       pc = int(pc[0]), int(pc[1])
       pd = int(pd[0]), int(pd[1])


       cv2.line(frame, pa, pb, (0, 255, 0), 2)
       cv2.line(frame, pb, pc, (0, 255, 0), 2)
       cv2.line(frame, pc, pd, (0, 255, 0), 2)
       cv2.line(frame, pd, pa, (0, 255, 0), 2)


       cen = r.center
       cen = int(cen[0]), int(cen[1])


       cv2.circle(frame, cen, 5, (255, 0, 0), -1)


       tag = r.tag_id
       cv2.putText(frame, str(tag), pa, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)


   cv2.imshow("frame", frame)


   if cv2.waitKey(1) == ord("q"):
    #    client.send("STP\n".encode("ascii"))
       break
cap.release()
cv2.destroyAllWindows()
host.close()