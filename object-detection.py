from ultralytics import YOLO
import json

def detect(image_path, model_path, cnf, mode, detected_foods):
    model = YOLO(model_path)
    # Model çıktılarını bastırmak için stdout'ı geçici bir StringIO nesnesine yönlendir

    results = model.predict(image_path, imgsz=800, conf=cnf, iou=0.45)
    json_object = results[0].tojson()
    json_array = json.loads(json_object)
    for item in json_array:
        detected_foods.append(item['name'])

def read_image_paths_from_txt(file_path):
    with open(file_path, 'r') as file:
        image_paths = [line.strip() for line in file.readlines()]
    return image_paths

def main():
    txt_file_path = 'images.txt'
    model_path = 'best.pt'
    confidence = 0.3
    mode = 1
    
    image_paths = read_image_paths_from_txt(txt_file_path)
    detected_foods = []
    
    for image_path in image_paths:
        detect(image_path, model_path, confidence, mode, detected_foods)
    
    # Benzersiz yiyecekler
    unique_foods = set(detected_foods)
    print("Detected foods:")
    print(unique_foods)


if __name__ == "__main__":
    main()
