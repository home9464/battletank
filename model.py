"""
https://github.com/google/automl/blob/master/efficientdet/README.md

curl -OL https://raw.githubusercontent.com/google-coral/test_data/master/efficientdet_lite3x_640_ptq.tflite
curl -OL https://raw.githubusercontent.com/google-coral/test_data/master/coco_labels.txt


# retrain

https://colab.research.google.com/github/google-coral/tutorials/blob/master/retrain_efficientdet_model_maker_tf2.ipynb

"""
import time
import os 

from tflite_runtime.interpreter import Interpreter 
from PIL import Image
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(dir_path, 'models', 'efficientdet_lite3x_640_ptq.tflite')
label_path = os.path.join(dir_path, 'models', 'coco_labels.txt')
true_labels = [line.strip() for line in open(label_path).readlines()]
#print(labels)

interpreter = Interpreter(model_path)
print("Model Loaded Successfully.")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
#print("Image Shape (", width, ",", height, ")")  # 640, 640

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load an image to be classified.
image_file = os.path.join(dir_path, 'cat.jpg')
image = Image.open(image_file).convert('RGB').resize((width, height))

start = time.time()
interpreter.set_tensor(input_details[0]['index'], np.expand_dims(image, 0))
interpreter.invoke()
predicted_sbounding_boxes = np.squeeze(interpreter.get_tensor(output_details[0]['index']))

predicted_label_indices = np.squeeze(interpreter.get_tensor(output_details[1]['index']))
predicted_scores = np.squeeze(interpreter.get_tensor(output_details[2]['index']))

idx = 0
label_idx = int(predicted_label_indices[idx])
score = predicted_scores[idx]

print(true_labels[label_idx], score, time.time()-start)
