import io
import os

from google.cloud import vision


# Set up credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\krish\Documents\GitHub\Hack-the-valley-project\credentials.json'

def detect_text():
    # Instantiate a client
    client = vision.ImageAnnotatorClient()

    # Load the image into memory
    with io.open(r'C:\Users\krish\Documents\GitHub\Hack-the-valley-project\backend\simpleprogram.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Detect text in the image
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Print the detected text
    text_combined = ""
    for text in texts:
        text_combined += text.description + " "
    return text_combined
