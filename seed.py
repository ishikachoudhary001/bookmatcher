import requests
from pymongo import MongoClient
import random

# --- MongoDB Connection ---
client = MongoClient("mongodb+srv://choudharyishika833_db_user:JIvg7ozmtKjHjjGh@bookmatcher.nagpfr9.mongodb.net/?appName=bookmatcher")
db = client["bookmatcher_db"]
books_collection = db["books"]

# --- Clear Existing Books ---
books_collection.delete_many({})
print("🧹 Cleared old books from MongoDB...")

# --- Step 1: Fetch Books from Open Library ---
print("📚 Fetching books from Open Library...")
openlibrary_books = []
genres = ["Romance", "Fiction", "Thriller", "Fantasy", "Science", "Self-Help", "Mystery"]

for genre in genres:
    try:
        url = f"https://openlibrary.org/subjects/{genre.lower()}.json?limit=150"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for work in data.get("works", []):
                book = {
                    "title": work.get("title", "Untitled"),
                    "author": work["authors"][0]["name"] if work.get("authors") else "Unknown",
                    "genre": genre,
                    "cover_url": f"https://covers.openlibrary.org/b/id/{work['cover_id']}-L.jpg"
                    if work.get("cover_id") else "https://via.placeholder.com/150x220.png?text=No+Cover",
                    "mood": random.choice(["Happy", "Sad", "Romantic", "Motivational", "Peaceful", "Adventurous"])
                }
                openlibrary_books.append(book)
        else:
            print(f"⚠️ Could not fetch {genre}")
    except Exception as e:
        print(f"Error fetching {genre}: {e}")

print(f"✅ Retrieved {len(openlibrary_books)} books from Open Library")

# --- Step 2: Add Your Custom Books ---
custom_books = [
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genre": "Fiction",
        "cover_url": "https://m.media-amazon.com/images/I/71aFt4+OTOL.jpg",
        "mood": "Motivational"
    },
    {
        "title": "It Ends With Us",
        "author": "Colleen Hoover",
        "genre": "Romance",
        "cover_url": "https://m.media-amazon.com/images/I/71pnJH+Rw-L.jpg",
        "mood": "Romantic"
    },
    {
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "genre": "Finance",
        "cover_url": "https://m.media-amazon.com/images/I/81Lb75rUhLL.jpg",
        "mood": "Thoughtful"
    },
    {
        "title": "The Mountain Is You",
        "author": "Brianna Wiest",
        "genre": "Self-Help",
        "cover_url": "https://m.media-amazon.com/images/I/71aLultW5EL.jpg",
        "mood": "Reflective"
    },
    {
        "title": "Eleanor Oliphant Is Completely Fine",
        "author": "Gail Honeyman",
        "genre": "Fiction",
        "cover_url": "https://m.media-amazon.com/images/I/71-8N-C0VSL.jpg",
        "mood": "Lonely"
    },
    {
        "title": "Ikigai: The Japanese Secret to a Long and Happy Life",
        "author": "Héctor García and Francesc Miralles",
        "genre": "Self-Help",
        "cover_url": "https://m.media-amazon.com/images/I/81l3rZK4lnL.jpg",
        "mood": "Peaceful"
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "Self-Improvement",
        "cover_url": "https://m.media-amazon.com/images/I/91bYsX41DVL.jpg",
        "mood": "Motivational"
    },
    {
        "title": "Every Time It Rains",
        "author": "Nikita Singh",
        "genre": "Romance",
        "cover_url": "https://m.media-amazon.com/images/I/81xZkO3X8VL.jpg",
        "mood": "Heartbroken"
    },
    {
        "title": "Way to You",
        "author": "Ishika Choudhary",
        "genre": "Romance",
        "cover_url": "/static/book_covers/way_to_you.jpg.PNG",  # Local file
        "mood": "Romantic"
    },
]

print("✨ Added your custom curated books!")

# --- Step 3: Combine & Insert ---
all_books = openlibrary_books + custom_books
books_collection.insert_many(all_books)

print(f"✅ Successfully seeded {len(all_books)} books into MongoDB!")

