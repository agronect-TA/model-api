import numpy as np
from PIL import Image
from tensorflow import keras
from information.model_info import corn_info
from keras.api.models import load_model

corn_model_path = 'model/corn_model.h5'
corn_model = load_model(corn_model_path)
corn_labels = ['Corn Healthy', 'Corn Gray Leaf Spot', 'Corn Common Rust', 'Corn Northern Leaf Blight']

def predict_corn(img):
    i = np.array(img) / 255.0
    if len(i.shape) == 3:
        i = i.reshape(1, 150, 150, 3)
    else:
        i = i.reshape(1, 150, 150, 1)
    
    pred = corn_model.predict(i)
    pred_class = np.argmax(pred)
    
    # Ensure confidence is a Python float
    confidence = float(pred[0][pred_class] * 100)  # Convert to float
    result = corn_labels[pred_class]
    info = corn_info[result]
    
    return result, confidence, info['description'], info['solution'], img

