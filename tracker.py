import cv2

# velocity of movement (pixels per sec), square (red/green), vector of an object not in the square

def put_text(text, coord):
    cv2.putText(img, text, coord, cv2.FONT_ITALIC, 1, (0, 0, 0), 2)

cap = cv2.VideoCapture(0)
cap.set(3, 500)
cap.set(4, 500)

faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

counter = 0
velocity_x = 0
velocity_y = 0
square_side_half = 100
face_center_previous = (cap.get(cv2.CAP_PROP_FRAME_WIDTH)//2, cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//2)

while True:
    success, img = cap.read()
    if not success: break

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    results = faces.detectMultiScale(img_gray, 2, 4)

    img_center = img.shape[1]//2, img.shape[0]//2
    left_point = img_center[0] - square_side_half
    right_point = img_center[0] + square_side_half
    top_point = img_center[1] - square_side_half
    bottom_point = img_center[1] + square_side_half

    cv2.rectangle(img, (left_point, top_point), (right_point, bottom_point), (0, 0, 255), 2)

    for (x, y, w, h) in results:
        face_center = x + (w // 2), y + (h // 2)

        if counter % cap.get(5) == 0:
            velocity_x = (face_center[0] - face_center_previous[0]) # neg - left, pos - right
            velocity_y = - (face_center[1] - face_center_previous[1]) # neg - down, pos - up
            # updating position once per sec
            face_center_previous = face_center

        to_the_left = face_center[0] < left_point
        to_the_right = face_center[0] > right_point
        upper = face_center[1] < top_point
        lower = face_center[1] > bottom_point

        if not (to_the_left or upper or to_the_right or lower):
            cv2.rectangle(img, (left_point, top_point), (right_point, bottom_point), (0, 255, 0), 2)
        elif to_the_left:
            put_text('LEFT', (10, 70))
        elif upper:
            put_text('UP', (10, 70))
        elif to_the_right:
            put_text('RIGHT', (10, 70))
        else:
            put_text('DOWN', (10, 70))

        put_text(f'Vx: {int(velocity_x)}, Vy: {int(velocity_y)}', (10, 30))

    counter += 1

    cv2.imshow('Camera Preview', img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cap.release()
cv2.destroyWindow('Camera Preview')