from ultralytics import YOLO
import json


def detect(image_path, model_path, cnf, mode):
    detected_foods = set()
    model = YOLO(model_path)
    # Model çıktılarını bastırmak için stdout'ı geçici bir StringIO nesnesine yönlendir

    results = model.predict(image_path, imgsz=800, conf=cnf, iou=0.45)
    json_object = results[0].tojson()
    json_array = json.loads(json_object)
    for item in json_array:
        detected_foods.add(item['name'])

    return detected_foods
