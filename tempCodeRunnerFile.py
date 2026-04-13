@app.route('/matcher', methods=['GET', 'POST'])
def matcher():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        mood = request.form.get('mood')
        books = list(mongo.db.books.find({"mood": mood}))
        return render_template('matcher.html', mood=mood, books=books)

    moods = ["Happy", "Sad", "Romantic", "Adventurous", "Calm", "Curious", "Motivated", "Dark"]
    return render_template('matcher.html', moods=moods)