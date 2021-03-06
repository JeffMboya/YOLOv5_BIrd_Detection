# -*- coding: utf-8 -*-
"""FYP-18-10 YOLOv5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y05dcyMQ3jAo2WIPqEvfgWsaWQ_0Z0U1
"""

import torch # YOLOv5 implemented using pytorch
from IPython.display import Image #this is to render predictions

#Clone YOLOv5 folder
!git clone https://github.com/ultralytics/yolov5

# Commented out IPython magic to ensure Python compatibility.
#change working directory to the yolov5 folder and install requirements
# %cd yolov5
!pip install -r requirements.txt

#Import required modules
!pip install IProgress
from tqdm import tqdm
import IProgress
from ipywidgets import IntProgress
torch.cuda.get_arch_list() 
print('All set. Using PyTorch version %s with %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

#Run the following lines of code to download the bird dataset from roboflow. 
!pip install roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="Insert your API key")
project = rf.workspace("ryu-myoungwoo").project("bird-detection-zqcdr")
dataset = project.version(5).download("yolov5")

# run this cell to begin training
!pip install wandb #For visualizing trainign progress
!python train.py --img 416 --batch 16 --epochs 50 --data data.yaml --weights yolov5s.pt --cache

# Let’s explore now how confident our model is. 
#We can plot a validation batch obtained during training and inspect the confidence score of each label as shown below
Image(filename='runs/train/exp3/val_batch2_labels.jpg', width=1000)

#Testing the YOLOv5 Model:
!python detect.py --weights /content/yolov5/runs/train/exp3/weights/best.pt --img 416 --conf 0.25 --source /content/yolov5/bird-detection-5/test/images

# Commented out IPython magic to ensure Python compatibility.
#Now that our custom YOLOv5 object detector has been verified, we might want to take the weights out of Colab for use on a live computer vision task. 
#To do so we import a Google Drive module and send them out.

from google.colab import drive
drive.mount('/content/gdrive')

# %cp /content/yolov5/runs/train/exp3/weights/best.pt /content/gdrive/My\ Drive

# Convert weights to fp16 TFLite model

!python export.py --weights /content/yolov5/runs/train/exp3/weights/best.pt --include tflite --img 416

# Lets run the created tflite model.

!python detect.py --weights /content/yolov5/runs/train/exp3/weights/best-fp16.tflite --img 416 --conf 0.25 --source /content/yolov5/bird-detection-5/test/images

#Convert weights to int8 TFLite model
!python export.py --weights /content/yolov5/runs/train/exp3/weights/best.pt --include tflite --int8 --img 416 --data data/coco128.yaml