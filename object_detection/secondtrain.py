import os
from yolov5 import train  # YOLOv5 repository's train script
import torch


# Eğitim için parametreler
train_params = {
    '--img': 640,  # giriş resim boyutu
    '--batch': 16,  # batch boyutu
    '--epochs': 100,  # epoch sayısı
    '--data': "C:/Users/Administrator/Desktop/2024 Son Okul Dönemim/Bil496/yolov5/data.yaml",  # veri konfigürasyon dosyası
    '--weights': 'yolov5m.pt',  # başlangıç ağırlıkları (örn. yolov5s.pt, yolov5m.pt, yolov5l.pt, yolov5x.pt)
    '--cache': None  # görüntüleri önbelleğe alır, eğitimi hızlandırır
}
if __name__ == '__main__':
    train.run(**train_params)
