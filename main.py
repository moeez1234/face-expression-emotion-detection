from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import io
from PIL import Image

app = FastAPI()

# Load model once when the server starts
model = load_model('emotion_model.hdf5', compile=False)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

@app.post("/predict")
async def predict_emotion(file: UploadFile = File(...)):
    # Read the image sent by the Pi
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('L') # Convert to Grayscale
    
    # Preprocess image to match your model (64x64)
    img_array = np.array(image.resize((64, 64)))
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=(0, -1))

    # Predict
    prediction = model.predict(img_array, verbose=0)[0]
    emotion_idx = np.argmax(prediction)
    
    return {"emotion": emotion_labels[emotion_idx], "confidence": float(np.max(prediction))}