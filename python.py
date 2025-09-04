from flask import Flask, render_template, session, request, redirect, url_for
import random
import math

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Change this!

# Sample movie data (replace with a real dataset)
movies = [
    {'id': 1, 'title': 'Movie A', 'genre': 'Comedy', 'poster': 'https://example.com/poster_a.jpg'},
    {'id': 2, 'title': 'Movie B', 'genre': 'Action', 'poster': 'https://example.com/poster_b.jpg'},
    {'id': 3, 'title': 'Movie C', 'genre': 'Comedy', 'poster': 'https://example.com/poster_c.jpg'},
    {'id': 4, 'title': 'Movie D', 'genre': 'Drama', 'poster': 'https://example.com/poster_d.jpg'},
    {'id': 5, 'title': 'Movie E', 'genre': 'Sci-Fi', 'poster': 'https://example.com/poster_e.jpg'},
    {'id': 6, 'title': 'Movie F', 'genre': 'Thriller', 'poster': 'https://example.com/poster_f.jpg'},
    {'id': 7, 'title': 'Movie G', 'genre': 'Romance', 'poster': 'https://example.com/poster_g.jpg'},
    {'id': 8, 'title': 'Movie H', 'genre': 'Action', 'poster': 'https://example.com/poster_h.jpg'},
    {'id': 9, 'title': 'Movie I', 'genre': 'Comedy', 'poster': 'https://example.com/poster_i.jpg'},
    {'id': 10, 'title': 'Movie J', 'genre': 'Drama', 'poster': 'https://example.com/poster_j.jpg'}
]

genres = ['Comedy', 'Action', 'Drama', 'Sci-Fi', 'Thriller', 'Romance']

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def calculate_similarity(user_genres, movie_genre):
    # Simple similarity: 1 if genre is in user_genres, 0 otherwise
    if movie_genre in user_genres:
        return 1
    return 0

def recommend_movies(user_genres, ratings, viewed_movies):
    recommended = []
    for movie in movies:
        if movie['id'] not in viewed_movies:
            similarity = calculate_similarity(user_genres, movie['genre'])
            if similarity > 0:
                score = similarity
                if movie['id'] in ratings:
                    score += ratings[movie['id']]  # Add rating to the score
                probability = sigmoid(score)
                recommended.append({'movie': movie, 'probability': probability * 100, 'reason': 'Genre match'})
    
    # Sort by probability
    recommended.sort(key=lambda x: x['probability'], reverse=True)
    return recommended

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['age'] = int(request.form['age'])
        session['genres'] = request.form.getlist('genres')
        session['ratings'] = {}
        session['viewed_movies'] = set()  # Track viewed movies
        return redirect(url_for('recommendations'))
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Movie Recommendation App - Sign Up</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .signup-container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); width: 500px; }
            h1 { text-align: center; color: #0056b3; }
            label { display: block; margin-bottom: 5px; color: #0056b3; }
            input[type="text"], input[type="number"], select, button { width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            button { background-color: #0056b3; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; transition: background-color 0.3s ease; }
            button:hover { background-color: #003d82; }
            .genre-options { display: flex; flex-direction: column; }
            .genre-options label { margin-bottom: 0; }
            .genre-options input[type="checkbox"] { width: auto; margin-right: 5px; }
        </style>
    </head>
    <body>
        <div class="signup-container">
            <h1>Sign Up for Movie Recommendations</h1>
            <form method="post">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required><br>
                
                <label for="age">Age:</label>
                <input type="number" id="age" name="age" required><br>
                
                <label>Genres:</label>
                <div class="genre-options">
                    <label><input type="checkbox" name="genres" value="Comedy"> Comedy</label>
                    <label><input type="checkbox" name="genres" value="Action"> Action</label>
                    <label><input type="checkbox" name="genres" value="Drama"> Drama</label>
                    <label><input type="checkbox" name="genres" value="Sci-Fi"> Sci-Fi</label>
                    <label><input type="checkbox" name="genres" value="Thriller"> Thriller</label>
                    <label><input type="checkbox" name="genres" value="Romance"> Romance</label>
                </div><br>
                
                <button type="submit">Get Recommendations</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/recommendations')
def recommendations():
    if 'name' not in session:
        return redirect(url_for('index'))

    user_genres = session['genres']
    ratings = session.get('ratings', {})
    viewed_movies = session.get('viewed_movies', set())
    recommended_movies = recommend_movies(user_genres, ratings, viewed_movies)
    return render_template('recommendations.html', movies=recommended_movies, name=session['name'])

@app.route('/rate/<int:movie_id>/<int:rating>')
def rate(movie_id, rating):
    if 'ratings' not in session:
        session['ratings'] = {}
    session['ratings'][movie_id] = rating
    session.modified = True  # Ensure session is saved
    session['viewed_movies'].add(movie_id)
    return redirect(url_for('recommendations'))

@app.route('/explore')
def explore():
    genre_filter = request.args.get('genre', 'All')
    
    filtered_movies = movies
    if genre_filter != 'All':
        filtered_movies = [movie for movie in movies if movie['genre'] == genre_filter]
    
    return render_template('explore.html', movies=filtered_movies, genres=genres, current_genre=genre_filter)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = next((movie for movie in movies if movie['id'] == movie_id), None)
    if movie is None:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)

@app.route('/watchlist/add/<int:movie_id>')
def add_to_watchlist(movie_id):
    if 'watchlist' not in session:
        session['watchlist'] = []
    if movie_id not in session['watchlist']:
        session['watchlist'].append(movie_id)
    session.modified = True
    return redirect(request.referrer)

@app.route('/watchlist')
def watchlist():
    watchlist_movies = [movie for movie in movies if movie['id'] in session.get('watchlist', [])]
    return render_template('watchlist.html', movies=watchlist_movies)

@app.route('/ratings')
def ratings():
    ratings = session.get('ratings', {})
    rated_movies = [(movie, rating) for movie in movies if movie['id'] in ratings for rating in [ratings[movie['id']]]]
    return render_template('ratings.html', rated_movies=rated_movies)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    search_results = [movie for movie in movies if query in movie['title'].lower()]
    return render_template('search.html', movies=search_results, query=query)

@app.template_string()
def render_template(template_name, **context):
    if template_name == 'recommendations.html':
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Movie Recommendations for {context['name']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 0; }}
                .container {{ width: 80%; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
                h1 {{ color: #0056b3; }}
                .movie-card {{ border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-bottom: 10px; display: flex; align-items: center; }}
                .movie-card img {{ width: 50px; height: 75px; margin-right: 10px; border-radius: 4px; }}
                .movie-card-info {{ flex-grow: 1; }}
                .movie-card-info h3 {{ margin-top: 0; color: #0056b3; }}
                .movie-card-info p {{ margin-bottom: 5px; }}
                .movie-card-rating a {{ display: inline-block; padding: 5px 10px; background-color: #0056b3; color: white; text-decoration: none; border-radius: 4px; margin-right: 5px; }}
                .movie-card-rating a:hover {{ background-color: #003d82; }}
                nav {{ background-color: #0056b3; padding: 10px; color: white; border-radius: 5px; margin-bottom: 20px; }}
                nav a {{ color: white; text-decoration: none; padding: 8px 12px; border-radius: 4px; margin-right: 10px; }}
                nav a:hover {{ background-color: #003d82; }}
                .link-button {{ display: inline-block; padding: 8px 12px; background-color: #0056b3; color: white; text-decoration: none; border-radius: 4px; margin-top: 10px; }}
                .link-button:hover {{ background-color: #003d82; }}
            </style>
        </head>
        <body>
            <div class="container">
                <nav>
                    <a href="/">Home</a>
                    <a href="/recommendations">Recommendations</a>
                    <a href="/explore">Explore</a>
                    <a href="/watchlist">Watchlist</a>
                    <a href="/ratings">My Ratings</a>
                    <a href="/search">Search</a>
                </nav>
                <h1>Movie Recommendations for {context['name']}</h1>
                {''.join([f"""
                    <div class="movie-card">
                        <img src="{movie['movie']['poster']}" alt="Movie Poster">
                        <div class="movie-card-info">
                            <h3>{movie['movie']['title']}</h3>
                            <p><strong>Genre:</strong> {movie['movie']['genre']}</p>
                            <p><strong>Why:</strong> {movie['reason']}</p>
                            <p><strong>Probability:</strong> {movie['probability']:.2f}%</p>
                            <div class="movie-card-rating">
                                <a href="/rate/{movie['movie']['id']}/1">Rate 1</a>
                                <a href="/rate/{movie['movie']['id']}/2">Rate 2</a>
                                <a href="/rate/{movie['movie']['id']}/3">Rate 3</a>
                                <a href="/rate/{movie['movie']['id']}/4">Rate 4</a>
                                <a href="/rate/{movie['movie']['id']}/5">Rate 5</a>
                            </div>
                            <a href="/movie/{movie['movie']['id']}" class="link-button">View Details</a>
                            <a href="/watchlist/add/{movie['movie']['id']}" class="link-button">Add to Watchlist</a>
                        </div>
                    </div>
                """ for movie in context['movies']])}
            </div>
        </body>
        </html>
        """
    elif template_name == 'explore.html':
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Explore Movies</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; margin: 0; padding: 0; }}
                .container {{ width: 80%; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
                h1 {{ color: #0056b3; }}
                .movie-grid {{ display: flex; flex-wrap: wrap; justify-content: space-around; }}
                .movie-card {{ width: 200px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; background-color: #f9f9f9; }}
                .movie-card img {{ width: 100%; height: auto; border-bottom: 1px solid #ddd; }}
                .movie-card-info {{ padding: 10px; }}
                .movie-card-info h3 {{ margin-top: 0; font-size: 1.2em; color: #0056b3; }}
                .movie-card-info p {{ margin-bottom: 5px; font-size: 0.9em; color: #666; }}
                .genre-filter {{ margin-bottom: 20px; }}
                .genre-filter a {{ display: inline-block; padding: 8px 12px; margin-right: 5px; background-color: #0056b3; color: white; text-decoration: none; border-radius: 4px; }}
                .genre-filter a:hover, .genre-filter a.active {{ background-color: #003d82; }}
                nav {{ background-color: #0056b3; padding: 10px; color: white; border-radius: 5px; margin-bottom: 20px; }}
                nav a {{ color: white; text-decoration: none; padding: 8px 12px; border-radius: 4px; margin-right: 10px; }}
                nav a:hover {{ background-color: #003d82; }}
                .link-button {{ display: inline-block; padding: 8px 12px; background-color: #0056b3; color: white; text-decoration: none; border-radius: 4px; margin-top: 10px; }}
                .link-button:hover {{ background-color: #003d82; }}
            </style>
        </head>
        <body>
            <div