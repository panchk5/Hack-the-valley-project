import io
import os

from google.cloud import vision
from google.cloud.vision import types

# Set up credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/path/to/your/credentials.json'

# Instantiate a client
client = vision.ImageAnnotatorClient()

# Load the image into memory
with io.open('/path/to/your/image.jpg', 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Detect text in the image
response = client.text_detection(image=image)
texts = response.text_annotations

# Print the detected text
for text in texts:
    print('\n"{}"'.format(text.description))
