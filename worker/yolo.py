import base64
import cv2
from ultralytics import YOLO
import time
import numpy as np
from PIL import Image 
from io import BytesIO
from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()
from django.conf import settings

model = YOLO('worker/models/best.pt')

def video_dectect(video_path = "worker/Driver turns across oncoming traffic - Earlwood NSW.mp4"):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'VP80')  # Change the fourcc code to 'VP80' for WebM
    output = cv2.VideoWriter('worker/static/video/output.webm', fourcc, 20.0, (width, height))
    start_time = time.time()
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        output.write(annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    output.release()
    print(f"--- {time.time() - start_time} seconds ---")
    return 'video/output.mp4'

def to_image(numpy_img):
    return Image.fromarray(numpy_img[:, :, ::-1], 'RGB')

def to_data_uri(pil_img):
    data = BytesIO()
    pil_img.save(data, "JPEG") # pick your format
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8') 

def image_detect(image_data = "website/worker/ezgif2.jpg"):
    image_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    results = model(image)
    accident = results[0].boxes.conf.item() > 0.75
    annotated_image = results[0].plot()
    pil_image = to_image(annotated_image)
    return to_data_uri(pil_image), accident

def notify_accident():
    account_sid = settings.ACC_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_=settings.PH_NO,
    body='ACCIDENT! Occured at 1234 Main Street',
    to=settings.MY_PH_NO
    )

    print(message.sid)