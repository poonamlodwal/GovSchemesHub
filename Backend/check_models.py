import os
from dotenv import load_dotenv
load_dotenv()
from google import genai

_raw_key = os.getenv("Gov_API_KEY")
if not _raw_key:
    print("Gov_API_KEY not set")
    exit(1)

client = genai.Client(api_key=_raw_key)

print("Available models:")
for m in client.models.list():
    print(m.name)


