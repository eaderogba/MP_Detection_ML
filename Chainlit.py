import chainlit as cl
from fastapi.testclient import TestClient
from inference import app 
import io
import os 


FASTAPI_URL = os.getenv('FASTAPI_URL', 'http://localhost:8000')

# Create a test client
client = TestClient(app, base_url=FASTAPI_URL)

async def process_image(image_file):
    # Read the file content
    with open(image_file.path, "rb") as f:
        file_content = f.read()
    
    # Create a file-like object
    file = io.BytesIO(file_content)
    
    # Send a request to your FastAPI app
    files = {"file": (image_file.name, file, image_file.type)}
    response = client.post("/MP_predict/", files=files)
    
    # Send the response back to the user
    result = response.json()
    await cl.Message(content=f"Image is: {result['prediction']}").send()

@cl.on_chat_start
async def prompt_for_image():
    files = await cl.AskFileMessage(
        content="Please upload an Image for Malaria Parasite detection.",
        accept=["image/jpeg", "image/png", "image/jpg"]
    ).send()
    
    if files:
        image_file = files[0]
        
        # Display the uploaded image
        image = cl.Image(path=image_file.path, name=image_file.name, display="inline")
        await cl.Message(content="Uploaded image:", elements=[image]).send()
        
        # Process the image
        await process_image(image_file)
    else:
        await cl.Message(content="No file was uploaded. Please try again.").send()

@cl.on_message
async def main(message: cl.Message):
    # For any message, prompt for a new image upload
    await prompt_for_image()