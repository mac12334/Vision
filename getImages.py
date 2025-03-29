import cv2

cap = cv2.VideoCapture(0)

counter = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    has, _ = cv2.findChessboardCorners(gray,(7, 7))
    if has:
        print("works" + str(counter))
        counter += 1

    cv2.imshow("name", gray)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()