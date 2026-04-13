from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
import os
import certifi

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")


mongo_uri = os.environ.get("MONGO_URI")

if not mongo_uri:
    raise Exception("MONGO_URI not found")

client = MongoClient(
    mongo_uri,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=3000,
    connectTimeoutMS=3000
)


db = client["bookmatcher_db"]
users = db["users"]
books = db["books"]

# Make datetime available in templates
@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

# Home redirects to login
@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            print("🔥 Signup started")

            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            if not username or not email or not password:
                return "Missing fields!"

            hashed_password = generate_password_hash(password)

            print("🔥 Checking existing user")
            existing_user = users.find_one({'email': email})

            if existing_user:
                return render_template('signup.html', error="Email already exists!")

            print("🔥 Inserting user")
            result = users.insert_one({
                'username': username,
                'email': email,
                'password': hashed_password
            })

            print("✅ Inserted ID:", result.inserted_id)

            return redirect(url_for('login'))

        return render_template('signup.html')

    except Exception as e:
        print("❌ Signup Error:", e)
        return f"Signup Error: {str(e)}"

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            print("🔥 Login started")

            email = request.form.get('email')
            password = request.form.get('password')

            print("🔥 Finding user")
            user = users.find_one({'email': email})

            if user and check_password_hash(user['password'], password):
                print("✅ Login success")
                session['user'] = {
                    '_id': str(user['_id']),
                    'username': user['username']
                }
                return redirect(url_for('dashboard'))

            return render_template('login.html', error="Invalid credentials.")

        return render_template('login.html')

    except Exception as e:
        print("❌ Login Error:", e)
        return f"Login Error: {str(e)}"

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    genres = {}
    for genre in db.books.distinct("genre"):
        # Sort by rating (highest first)
        books = list(db.books.find({"genre": genre}).sort("rating", -1))
        genres[genre] = books
    return render_template('dashboard.html', books_by_genre=genres)


@app.route('/matcher', methods=['GET', 'POST'])
def matcher():
    moods = ["Happy", "Sad", "Adventurous", "Romantic", "Motivated", "Calm"]

    if request.method == 'POST':
        mood = request.form.get('mood')
        matching_books = list(books.find({"mood": mood}))
        return render_template('matcher.html', moods=moods, mood=mood, books=matching_books)
    
    return render_template('matcher.html', moods=moods, mood=None, books=None)




# Book Detail
from bson import ObjectId

@app.route("/book/<book_id>")
def book_detail(book_id):
    book = books.find_one({"_id": ObjectId(book_id)})
    return render_template("book_detail.html", book=book)
@app.route('/feedback/<book_id>', methods=['POST'])
def feedback(book_id):
    feedback_text = request.form.get('feedback')
    rating = request.form.get('rating')
    username = session.get('username', 'Anonymous')
    feedback_entry = {
        'book_id': ObjectId(book_id),
        'user': username,
        'feedback': feedback_text,
        'rating': rating,
        'date': datetime.utcnow()
    }
    db.feedbacks.insert_one(feedback_entry)
    return redirect(url_for('book_detail', book_id=book_id))


# Search
@app.route('/search_books')
def search_books():
    query = request.args.get('q', '')
    results = list(books.find({'title': {'$regex': query, '$options': 'i'}}))
    return render_template('dashboard.html', books_by_genre={'Search Results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
