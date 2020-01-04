import cv2

first_frame = None
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)
    if first_frame is None:
        first_frame = blur
        print(first_frame)
        continue
    delta_frame = cv2.absdiff(first_frame, blur)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnt, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for counter in cnt:
        if cv2.contourArea(counter) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(counter)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Windows", frame)

    k = cv2.waitKey(1)
    if k == ord("q"):
        break
        video.release()
        cv2.destroyAllWindows()
