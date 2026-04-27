import cv2
import datetime
import smtplib
import ssl
from email.message import EmailMessage
import csv
import os
import time

# ---------------- EMAIL CONFIG ----------------
SENDER_EMAIL = "venkatasaideepthi3@gmail.com"
APP_PASSWORD = ""
RECEIVER_EMAIL = "receiver_email@gmail.com"

# ---------------- LOAD FACE MODEL ----------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- CREATE LOG FILE ----------------
if not os.path.exists("intrusion_log.csv"):
    with open("intrusion_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Person Type", "Image Name"])

# ---------------- EMAIL FUNCTION ----------------
def send_email(image_path):
    msg = EmailMessage()
    msg["Subject"] = "⚠ Intrusion Alert - Unknown Person!"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content("Unknown person detected. See attached image.")

    with open(image_path, "rb") as img:
        msg.add_attachment(
            img.read(),
            maintype="image",
            subtype="jpeg",
            filename=os.path.basename(image_path)
        )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# ---------------- START CAMERA ----------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Smart Home Intrusion System Started")
print("Press 'k' if Known person, otherwise treated as Unknown")

last_email_time = 0
cooldown = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    key = cv2.waitKey(1) & 0xFF

    for (x, y, w, h) in faces:

        person_type = "Unknown"
        color = (0, 0, 255)  # Red default

        if key == ord('k'):
            person_type = "Known"
            color = (0, 255, 0)

        timestamp_display = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, f"{person_type} | {timestamp_display}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        image_name = f"{person_type}_{timestamp_file}.jpg"
        cv2.imwrite(image_name, frame)

        # Log
        with open("intrusion_log.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp_display, person_type, image_name])

        # Email only for Unknown
        if person_type == "Unknown":
            current_time = time.time()
            if current_time - last_email_time > cooldown:
                print(f"⚠ Unknown detected at {timestamp_display}")
                send_email(image_name)
                print("Email Sent!")
                last_email_time = current_time

    cv2.imshow("Smart Home Intrusion Detection", frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
