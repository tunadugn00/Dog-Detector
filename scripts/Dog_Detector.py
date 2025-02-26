import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os

# Import thông tin về giống chó
from .dog_breeds_info import get_breed_info

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
MODEL_PATH = os.path.join(BASE_DIR, "models", "dog_breeds_classifier_model.h5")  

model = tf.keras.models.load_model(MODEL_PATH)

class_names = [
    "Affenpinscher", "Airedale", "Appenzeller", "Basenji", "Basset", "Beagle", 
    "Bloodhound", "Bluetick", "Borzoi", "Boxer", "Briard", "Bull", "Cairn", 
    "Cardigan", "Chihuahua", "Chow", "Clumber", "Collie", "Dhole", "Dingo", 
    "Doberman", "EntleBucher", "Groenendael", "Husky", "Keeshond", "Kelpie", 
    "Komondor", "Kuvasz", "Leonberg", "Lhasa", "Malamute", "Malinois", 
    "Otterhound", "Papillon", "Pekinese", "Pembroke", "Pomeranian", "Pug", 
    "Redbone", "Rottweiler", "Saluki", "Samoyed", "Schipperke", "Vizsla", 
    "Weimaraner", "Whippet"
]

def classify_image(img_path):
    try:
        if hasattr(model, 'input_shape'):
            input_shape = model.input_shape
            height, width = input_shape[1:3]
            print(f"Lấy kích thước từ model.input_shape: {height}x{width}")
        elif hasattr(model, 'layers') and len(model.layers) > 0:
            if hasattr(model.layers[0], 'input_shape'):
                input_shape = model.layers[0].input_shape
                height, width = input_shape[1:3]
                print(f"Lấy kích thước từ lớp đầu tiên: {height}x{width}")
            else:
                height, width = 224, 224
                print(f"Sử dụng kích thước mặc định: {height}x{width}")
        else:
            height, width = 224, 224
            print(f"Sử dụng kích thước mặc định: {height}x{width}")
    except Exception as e:
        print(f"Lỗi khi xác định kích thước đầu vào: {e}")
        height, width = 224, 224
        print(f"Sử dụng kích thước mặc định: {height}x{width}")
    
    img = image.load_img(img_path, target_size=(height, width))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class]

    if confidence > 0.5:
        breed_name = class_names[predicted_class]
        breed_info = get_breed_info(breed_name)
        
        result = {
            "breed": breed_name,
            "confidence": float(confidence),
            "description": breed_info["description"],
            "origin": breed_info["origin"],
            "life_span": breed_info["life_span"],
            "temperament": breed_info["temperament"],
            "height": breed_info["height"],
            "weight": breed_info["weight"],
            "colors": breed_info["colors"]
            
        }
        
        return result
    else:
        return {"breed": None, "message": "This picture is not of a dog."}