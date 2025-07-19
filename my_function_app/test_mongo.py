from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
load_dotenv()
import os


uri = os.getenv("MONGO_URI")
client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())

try:
    client.admin.command("ping")
    print("✅ MongoDB connection successful!")
    print(os.getenv("MONGO_URI"))
except Exception as e:
    print("❌ MongoDB connection failed:", e)