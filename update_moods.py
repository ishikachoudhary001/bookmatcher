from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["bookmatcher_db"]
books = db["books"]

# Define possible moods
moods = ["Happy", "Sad", "Adventurous", "Romantic", "Motivated", "Calm"]

# Add a random mood to each book if it doesn't have one
for book in books.find():
    if "mood" not in book or not book["mood"]:
        new_mood = random.choice(moods)
        books.update_one({"_id": book["_id"]}, {"$set": {"mood": new_mood}})
        print(f"Updated {book['title']} → {new_mood}")

print("✅ All books now have a mood!")
