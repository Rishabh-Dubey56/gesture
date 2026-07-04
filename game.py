import cv2
import mediapipe as mp
import random
import time
import numpy as np

# -----------------------
# Initialize MediaPipe
# -----------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

WIDTH = 1280
HEIGHT = 720
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

# -----------------------
# Game Variables
# -----------------------
balloons = []
score = 0
level = 1
game_duration = 60
start_time = None
game_started = False

# -----------------------
# Balloon Creation
# -----------------------
def create_balloon():
    x = random.randint(100, WIDTH - 100)
    y = -50
    radius = random.randint(30, 45)
    speed = random.randint(3 + level, 6 + level)
    color = (
        random.randint(50,255),
        random.randint(50,255),
        random.randint(50,255)
    )
    balloons.append([x, y, radius, speed, color])

# -----------------------
# Background Gradient
# -----------------------
def draw_gradient_background(canvas):
    for i in range(HEIGHT):
        color = (255 - i//3, 200 - i//4, 255)
        cv2.line(canvas, (0, i), (WIDTH, i), color, 1)

# -----------------------
# Start Screen
# -----------------------
def draw_start_screen(canvas):
    draw_gradient_background(canvas)
    cv2.putText(canvas, "AI Balloon Pop Game",
                (WIDTH//2 - 300, HEIGHT//2 - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 4)
    cv2.putText(canvas, "Show Index Finger to Start",
                (WIDTH//2 - 300, HEIGHT//2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (50,50,50), 3)

# -----------------------
# Game Loop
# -----------------------
while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    if not game_started:
        draw_start_screen(canvas)

        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0].landmark[8]
            if lm.y < results.multi_hand_landmarks[0].landmark[6].y:
                game_started = True
                start_time = time.time()
                for _ in range(5):
                    create_balloon()

    else:
        draw_gradient_background(canvas)

        elapsed = int(time.time() - start_time)
        remaining = game_duration - elapsed

        cursor_x, cursor_y = 0, 0

        if results.multi_hand_landmarks:
            handLms = results.multi_hand_landmarks[0]
            lm = handLms.landmark[8]
            cursor_x = int(lm.x * WIDTH)
            cursor_y = int(lm.y * HEIGHT)

            cv2.circle(canvas, (cursor_x, cursor_y),
                       15, (255, 0, 255), -1)

        # Update balloons
        for balloon in balloons[:]:
            balloon[1] += balloon[3]
            cv2.circle(canvas, (balloon[0], balloon[1]),
                       balloon[2], balloon[4], -1)

            distance = np.sqrt((cursor_x - balloon[0])**2 +
                               (cursor_y - balloon[1])**2)

            if distance < balloon[2]:
                balloons.remove(balloon)
                score += 1
                if score % 5 == 0:
                    level += 1
                create_balloon()

            if balloon[1] > HEIGHT:
                balloons.remove(balloon)
                create_balloon()

        # Dashboard Panel
        cv2.rectangle(canvas, (0,0), (WIDTH,80), (30,30,30), -1)
        cv2.putText(canvas, f"Score: {score}",
                    (30,50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,255,0), 3)

        cv2.putText(canvas, f"Level: {level}",
                    (300,50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255,255,0), 3)

        cv2.putText(canvas, f"Time: {remaining}",
                    (600,50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,0,255), 3)

        # Webcam Preview (Top Right Corner)
        small_cam = cv2.resize(frame, (250, 180))
        canvas[100:280, WIDTH-270:WIDTH-20] = small_cam

        if remaining <= 0:
            cv2.putText(canvas, "TIME OUT",
                        (WIDTH//2 - 250, HEIGHT//2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0,0,255), 5)
            cv2.imshow("AI Balloon Game", canvas)
            cv2.waitKey(5000)
            break

    cv2.imshow("AI Balloon Game", canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()