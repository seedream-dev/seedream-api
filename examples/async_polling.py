"""Fire-and-poll: submit without blocking, do other work, then collect the result."""
import time
from seedream_api import Client

client = Client()  # reads SYNEXA_API_KEY
prediction = client.run({"prompt": "Replace the sky with a dramatic sunset, keep everything else exactly as it is", "image_urls": ["https://example.com/input.png"]}, wait=False)
print("submitted", prediction["id"], prediction["status"])
while prediction["status"] not in ("succeeded", "failed"):
    time.sleep(2)
    prediction = client.get(prediction["id"])
print(prediction["status"], prediction.get("output"))
