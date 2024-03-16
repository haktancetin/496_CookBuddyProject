import torch
import cv2

# Modeli
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Video dosyasını
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# Video çözünürlüğünü al
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    results = model(frame)


    results.show()

    # Sonuçları işleme
    # (opsiyonel) Sonuçları çizme, kaydetme, vb.

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
