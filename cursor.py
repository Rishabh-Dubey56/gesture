import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time

# ---------------- SETUP ----------------
pyautogui.FAILSAFE = True

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Camera not opening")
    exit()

screen_w, screen_h = pyautogui.size()

last_click = 0
prev_time = 0
fps = 0

print("🚀 AI GESTURE DASHBOARD STARTED")

# ---------------- DASHBOARD FUNCTION ----------------
def draw_dashboard(frame, gesture, fps):
    h, w, _ = frame.shape

    # Top panel
    cv2.rectangle(frame, (0, 0), (w, 80), (20, 20, 20), -1)

    cv2.putText(frame, "AI GESTURE CONTROL SYSTEM", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.putText(frame, f"GESTURE: {gesture}", (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (300, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # Right panel
    cv2.rectangle(frame, (w-220, 80), (w, 250), (30, 30, 30), -1)

    cv2.putText(frame, "STATUS", (w-200, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.putText(frame, "ACTIVE", (w-200, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if gesture == "CLICK":
        cv2.putText(frame, "CLICKED!", (w-200, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return frame

# ---------------- LOOP ----------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "NO HAND"

    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:

            lm = [(int(p.x * w), int(p.y * h)) for p in hand.landmark]

            x, y = lm[8]

            sx = np.interp(x, [0, w], [0, screen_w])
            sy = np.interp(y, [0, h], [0, screen_h])

            pyautogui.moveTo(sx, sy)

            dist = np.hypot(lm[4][0] - x, lm[4][1] - y)

            if dist < 40:
                gesture = "CLICK"
                now = time.time()

                if now - last_click > 1:
                    pyautogui.click()
                    last_click = now

            else:
                gesture = "MOVE"

    # ---------------- FPS CALC ----------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    # ---------------- UI DASHBOARD ----------------
    frame = draw_dashboard(frame, gesture, fps)

    cv2.imshow("🚀 AI GESTURE CONTROL DASHBOARD", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()