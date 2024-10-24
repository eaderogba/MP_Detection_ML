import uvicorn
from fastapi import FastAPI,File, UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io



# Load the model 
model = tf.keras.models.load_model("MP_Detection_ML.h5")
app = FastAPI()
def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Preprocess the image for the model.
    Modify this function according to your model's preprocessing requirements.
    """
    image = image.resize((128, 128))  # Resize image to match model input size
    image = np.array(image) / 255.0   # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image
@app.post("/MP_predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()

    # Convert bytes data to a PIL Image
    image = Image.open(io.BytesIO(contents))

    # Preprocess the image
    input_data = preprocess_image(image)

    # Make a prediction
    prediction = model.predict(input_data)

    result = "Uninfected" if prediction[0][0] > 0.5 else "Parasitized"

    return {"filename": file.filename, "prediction": result}
# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)