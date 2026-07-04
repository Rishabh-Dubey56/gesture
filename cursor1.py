import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8,
                       min_tracking_confidence=0.8)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

cooldown = 1
last_action = 0

def finger_up(tip, pip):
    return (pip.y - tip.y) > 0.03  # slightly relaxed margin

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            lm = hand_landmarks.landmark

            index = finger_up(lm[8], lm[6])
            middle = finger_up(lm[12], lm[10])
            ring = finger_up(lm[16], lm[14])
            pinky = finger_up(lm[20], lm[18])

            total = sum([index, middle, ring, pinky])

            current_time = time.time()

            if current_time - last_action > cooldown:

                # Index only → Scroll Up
                if index and not middle and not ring and not pinky:
                    pyautogui.scroll(80)
                    print("Scroll Up")
                    last_action = current_time

                # Index + Middle → Scroll Down
                elif index and middle and not ring and not pinky:
                    pyautogui.scroll(-80)
                    print("Scroll Down")
                    last_action = current_time

                # Fist → Zoom In
                elif total == 0:
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('=')
                    pyautogui.keyUp('ctrl')
                    print("Zoom In")
                    last_action = current_time

                # Open Palm → Zoom Out
                elif total == 4:
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('-')
                    pyautogui.keyUp('ctrl')
                    print("Zoom Out")
                    last_action = current_time

            mp_draw.draw_landmarks(img,
                                   hand_landmarks,
                                   mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Control Stable", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()