import cv2
import apriltag
import numpy
import math
import socket
import convert_to_dict

cap = cv2.VideoCapture(0)
op = apriltag.DetectorOptions("tag36h11")
detect = apriltag.Detector(op)


calib = numpy.load("calibration_data.npz")
cam_mtx = calib["camera_matrix"]
camera_params = [cam_mtx[0, 0], cam_mtx[1, 1], cam_mtx[0, 2], cam_mtx[1, 2]]

host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host.bind(("0.0.0.0", 9480))
host.listen(1)

apriltagData = convert_to_dict.allInOne("./apriltags.txt")

client, _ = host.accept()
s = ""

def sendRel(cli: socket.socket, sendable: str) -> None:
  	cli.send(sendable.encode("ascii"))

def sendFieldRel(cli: socket.socket, id: int, fX: float, fY: float) -> None:
  	cli.send(f"{id},{int(fX * 1000)},{int(fY * 1000)}\n".encode("ascii"))

while True:
	rec = client.recv(1024).decode()
	print(rec)

	res, frame = cap.read()

	if not res:
		print("failed to load")
		break
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	result = detect.detect(gray)


	if len(result) == 0:
		s = "0,0,0,0\n"

	actualX, actualY = 0, 0
	id = 0

	for r in result:
		arr, _, _ = detect.detection_pose(r, camera_params)
		yaw = math.atan2(arr[1][0], arr[0][0])
		pitch = math.atan2(-arr[2][0], math.sqrt(arr[2][1]**2 + arr[2][2]**2))
		roll = math.atan2(arr[2][1], arr[2][2])

		# the metrics is assuming the apriltag is 1 unit by 1 unit to fix this you need to multiply by the height of the apriltag and divide it by 12

		# roboY you need to inverse x to get the y of the robot, Y is left of the robot
		roboY = (((arr[0][3] * -1) * 0.15875))
		# roboX you need to use z to get x, basically X is forward
		roboX = (((arr[2][3]) * 0.15875))
		
		#roboTheta gets the angle from roboY and the nearest apriltag
		roboTheta = -(math.degrees(yaw))

		# put the current position to be relative to the field
		apRefPos = apriltagData[r.tag_id]
		
		s = f"{r.tag_id},{int(roboX * 1000)},{int(roboY * 1000)},{int(roboTheta * 1000)}\n"
		actualX = (roboX * math.cos(apRefPos[2])) - (roboY * math.sin(apRefPos[2]))
		actualY = (roboX * math.sin(apRefPos[2])) + (roboY * math.cos(apRefPos[2]))
		id = r.tag_id

	if rec == "PLS\n":
		sendRel(client, s)
		print("got here")
	else:
		print("not here")
		sendFieldRel(client, id, actualX, actualY)

	if cv2.waitKey(1) == ord("q"):
		client.send("STP\n".encode("ascii"))
		break
cap.release()
cv2.destroyAllWindows()
host.close()