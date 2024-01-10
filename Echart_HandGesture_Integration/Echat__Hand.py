import cv2
import mediapipe as mp
from keras.models import load_model
import numpy as np
import time
import random
from collections import Counter

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
model = load_model('emojinator_v3.h5')

image_x, image_y = 200, 200

cap = cv2.VideoCapture(0)

def overlay(image, pred_class, x, y, w, h):
    label = get_label(pred_class)
    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return image, label

def get_label(pred_class):
    if pred_class == 0:
        return "Up"
    elif pred_class == 1:
        return "Right"
    elif pred_class == 2:
        return "Down"
    elif pred_class == 3:
        return "Left"
    else:
        return "Unknown"

def display_rotated_e_chart(orientation):
    # Define the size of the E chart image
    chart_size = (1000, 800)

    # Create a blank white image as the background
    e_chart = np.ones((chart_size[0], chart_size[1], 3), np.uint8) * 255

    # Draw the E letter at the center of the chart
    cv2.putText(e_chart, "E", (chart_size[0] // 2 - 20, chart_size[1] // 2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)

    # Rotate the E based on the orientation
    if orientation == "Right":
        rotated_e_chart = e_chart
    elif orientation == "Down":
        rotated_e_chart = cv2.rotate(e_chart, cv2.ROTATE_90_CLOCKWISE)
    elif orientation == "Left":
        rotated_e_chart = cv2.rotate(e_chart, cv2.ROTATE_180)
    elif orientation == "Up":
        rotated_e_chart = cv2.rotate(e_chart, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Display the rotated E chart in a new window
    cv2.imshow("E Chart", rotated_e_chart)

    # Return the rotated E chart and orientation name
    return rotated_e_chart, orientation

def display_report_window(report):
    # Create a new window to display the report
    report_window_size = (600, 100)
    report_window = np.ones((report_window_size[1], report_window_size[0], 3), np.uint8) * 255
    cv2.putText(report_window, report, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.imshow("Report", report_window)

def main():
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    hand_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=5)
    hand_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=10, circle_radius=10)

    label_history = []
    orientation_history = []
    start_time = time.time()

    # Initialize the E chart orientation
    current_e_orientation = None
    start_time = time.time()

    while cap.isOpened():
        # Randomly choose a new orientation for the E chart every 5 seconds
        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            orientations = ["Up", "Right", "Down", "Left"]
            current_e_orientation = random.choice(orientations)
            rotated_e_chart, _ = display_rotated_e_chart(current_e_orientation)
            start_time = time.time()

        ret, image = cap.read()
        image = cv2.flip(image, 1)
        image_orig = cv2.flip(image, 1)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results_hand = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results_hand.multi_hand_landmarks:
            for hand_landmarks in results_hand.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=hand_landmarks,
                    connections=mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=hand_landmark_drawing_spec,
                    connection_drawing_spec=hand_connection_drawing_spec)
                res = cv2.bitwise_and(image, cv2.bitwise_not(image_orig))

                gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
                ret, th1 = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if len(contours) > 0:
                    contours = sorted(contours, key=cv2.contourArea)
                    contour = contours[-1]
                    x1, y1, w1, h1 = cv2.boundingRect(contour)
                    cv2.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                    save_img = gray[y1:y1 + h1, x1:x1 + w1]
                    save_img = cv2.resize(save_img, (image_x, image_y))
                    pred_probab, pred_class = keras_predict(model, save_img)
                    print(pred_class, pred_probab)

                    image, label = overlay(image, pred_class, x1 + 70, y1 - 120, 90, 90)
                    label_history.append(label)

        keypress = cv2.waitKey(1)
        if keypress == ord('q'):
            break

        cv2.imshow("Img", image)

        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            most_common_label = Counter(label_history).most_common(1)
            if most_common_label:
                print("Most Common Label:", most_common_label[0][0])

                # Store the E chart orientation label
                orientation_history.append(current_e_orientation)

                # Compare gesture label with the orientation of the displayed E chart
                if most_common_label[0][0] == current_e_orientation:
                    result = "Correct"
                else:
                    result = "Wrong"

                # Display the result as a report
                report = f"E Chart Label: {current_e_orientation}, Gesture Label: {most_common_label[0][0]}, Result: {result}"
                print(report)

                # Display the report in a separate window
                display_report_window(report)

            label_history = []  # Clear the label history

    hands.close()
    cap.release()
    cv2.destroyAllWindows()

def keras_predict(model, image):
    processed = keras_process_image(image)
    pred_probab = model.predict(processed)[0]
    pred_class = np.argmax(pred_probab)
    return max(pred_probab), pred_class

def keras_process_image(img):
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, image_x, image_y, 1))
    return img

if __name__ == "__main__":
    main()
