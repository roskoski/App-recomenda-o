import os
import math
import random
from flask import Flask, render_template_string, request, redirect, url_for, session

# Define a aplicação Flask e a chave secreta para a sessão
app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- Mock Data: Dados de Filmes para o Catálogo (Substitua por uma API de verdade em produção) ---
# Os dados são propositalmente simplificados para a demonstração
MOVIES = [
    {
        'id': 1, 'title': 'O Senhor dos Anéis: A Sociedade do Anel', 'year': 2001,
        'genres': ['Fantasia', 'Aventura', 'Ação'], 'popularity': 0.95,
        'poster_url': 'https://image.tmdb.org/t/p/w500/rC7JgS3h8E4y8P6q7P4G5q8g8f5.jpg',
        'plot': 'Um hobbit de um pacato condado herda um anel mágico e embarca em uma jornada para destruir o artefato e salvar a Terra Média.'
    },
    {
        'id': 2, 'title': 'Pulp Fiction: Tempos de Violência', 'year': 1994,
        'genres': ['Crime', 'Drama'], 'popularity': 0.92,
        'poster_url': 'https://image.tmdb.org/t/p/w500/uB2t4q10W30uP9r5dG7s4l9f7aQ.jpg',
        'plot': 'A vida de dois assassinos de aluguel, um boxeador, a esposa de um gângster e dois ladrões de lanchonete se entrelaçam em uma série de eventos violentos e cômicos.'
    },
    {
        'id': 3, 'title': 'Forrest Gump: O Contador de Histórias', 'year': 1994,
        'genres': ['Drama', 'Romance'], 'popularity': 0.94,
        'poster_url': 'https://image.tmdb.org/t/p/w500/e9Q0RjU9m7v18jCgPj1s4Xz9P1.jpg',
        'plot': 'A história da vida de um homem de bom coração com um QI baixo que, sem querer, testemunha e influencia muitos dos eventos históricos do século XX.'
    },
    {
        'id': 4, 'title': 'A Origem', 'year': 2010,
        'genres': ['Ficção Científica', 'Ação', 'Suspense'], 'popularity': 0.96,
        'poster_url': 'https://image.tmdb.org/t/p/w500/3U6F9P8b5q5R9wX8U6o9gQ7Q9jP.jpg',
        'plot': 'Um ladrão com a rara habilidade de invadir sonhos e roubar segredos de mentes subconscientes recebe a tarefa de plantar uma ideia na mente de um magnata.'
    },
    {
        'id': 5, 'title': 'Interestelar', 'year': 2014,
        'genres': ['Ficção Científica', 'Aventura', 'Drama'], 'popularity': 0.98,
        'poster_url': 'https://image.tmdb.org/t/p/w500/uR8rU10t2jD7g00nBf1704e6JjY.jpg',
        'plot': 'Uma equipe de exploradores viaja através de um buraco de minhoca no espaço em uma tentativa de garantir a sobrevivência da humanidade.'
    },
    {
        'id': 6, 'title': 'Parasita', 'year': 2019,
        'genres': ['Comédia', 'Drama', 'Suspense'], 'popularity': 0.97,
        'poster_url': 'https://image.tmdb.org/t/p/w500/6y18h07sO6oD5gXw1W0T5m5x6K.jpg',
        'plot': 'Uma família desempregada de vida simples se infiltra na casa de uma família rica, dando início a uma série de eventos inesperados e sombrios.'
    },
    {
        'id': 7, 'title': 'O Poderoso Chefão', 'year': 1972,
        'genres': ['Crime', 'Drama'], 'popularity': 0.99,
        'poster_url': 'https://image.tmdb.org/t/p/w500/e6vXg8J5wJ6mXvF4n5S6b3G7CjG.jpg',
        'plot': 'O patriarca de uma família da máfia de Nova York passa o controle de seu império clandestino para seu filho relutante.'
    },
    {
        'id': 8, 'title': 'O Cavaleiro das Trevas', 'year': 2008,
        'genres': ['Ação', 'Crime', 'Drama'], 'popularity': 0.96,
        'poster_url': 'https://image.tmdb.org/t/p/w500/qJ2yB22L0vW0mG61G9vB2G9G7wN.jpg',
        'plot': 'Batman se une a um novo promotor de justiça, Harvey Dent, para desmantelar o crime organizado em Gotham, mas um novo vilão enigmático conhecido como o Coringa aterroriza a cidade.'
    },
    {
        'id': 9, 'title': 'Matrix', 'year': 1999,
        'genres': ['Ficção Científica', 'Ação'], 'popularity': 0.93,
        'poster_url': 'https://image.tmdb.org/t/p/w500/f8s5l4w71vG1K3cK5oJ7v2x6f3r.jpg',
        'plot': 'Um hacker descobre que a realidade é uma simulação de computador criada por máquinas e se junta a um grupo de rebeldes para lutar contra elas.'
    },
    {
        'id': 10, 'title': 'Cidade de Deus', 'year': 2002,
        'genres': ['Crime', 'Drama'], 'popularity': 0.91,
        'poster_url': 'https://image.tmdb.org/t/p/w500/vQvj7g29j0g4a2z1R5V161wJ5rG.jpg',
        'plot': 'A história de dois amigos que crescem em um bairro violento do Rio de Janeiro, com um se tornando um fotógrafo e o outro um traficante.'
    },
    {
        'id': 11, 'title': 'Whiplash: Em Busca da Perfeição', 'year': 2014,
        'genres': ['Drama', 'Música'], 'popularity': 0.89,
        'poster_url': 'https://image.tmdb.org/t/p/w500/fW6F1t57qfEa6rL0sY5d9N3D2gY.jpg',
        'plot': 'Um jovem e promissor baterista de jazz matricula-se em uma conservatória de música de elite, onde é treinado por um professor temido e impiedoso.'
    },
    {
        'id': 12, 'title': 'O Labirinto do Fauno', 'year': 2006,
        'genres': ['Fantasia', 'Drama', 'Guerra'], 'popularity': 0.88,
        'poster_url': 'https://image.tmdb.org/t/p/w500/y4f95WdE1K8rJ8Rz6C5y8N6Q8f7.jpg',
        'plot': 'Na Espanha de 1944, uma jovem garota escapa para um mundo de fantasia para fugir da guerra e da tirania de seu padrasto, um cruel oficial do exército.'
    },
    {
        'id': 13, 'title': 'Mad Max: Estrada da Fúria', 'year': 2015,
        'genres': ['Ação', 'Ficção Científica', 'Aventura'], 'popularity': 0.90,
        'poster_url': 'https://image.tmdb.org/t/p/w500/qj8fG9gQ0vQ4a8z7K4g5k3N6p8x.jpg',
        'plot': 'Em um futuro pós-apocalíptico, uma imperatriz rebelde e um nômade chamado Max Rockatansky fogem de um senhor da guerra e sua gangue em uma perseguição frenética pelo deserto.'
    },
    {
        'id': 14, 'title': 'O Resgate do Soldado Ryan', 'year': 1998,
        'genres': ['Guerra', 'Drama'], 'popularity': 0.93,
        'poster_url': 'https://image.tmdb.org/t/p/w500/80uOqM3Oq1i2N5y0f4q7f0g2b7P.jpg',
        'plot': 'Durante a Segunda Guerra Mundial, um grupo de soldados americanos é enviado em uma missão perigosa atrás das linhas inimigas para resgatar um paraquedista que perdeu todos os seus irmãos em combate.'
    },
    {
        'id': 15, 'title': 'O Grande Lebowski', 'year': 1998,
        'genres': ['Comédia', 'Crime'], 'popularity': 0.87,
        'poster_url': 'https://image.tmdb.org/t/p/w500/qMhPqj9XfB4p0z3q7Xz9T7Y5S6.jpg',
        'plot': 'Um cara preguiçoso é confundido com um milionário e se envolve em uma conspiração criminosa complexa e bizarra.'
    },
]

# Gêneros de filmes para o formulário de cadastro
MOVIE_GENRES = sorted(list(set(g for m in MOVIES for g in m['genres'])))

# --- Lógica do Motor de Recomendação ---

def get_movies_by_id(movie_id):
    """Retorna um filme pelo ID."""
    return next((m for m in MOVIES if m['id'] == movie_id), None)

def get_user_profile():
    """Busca o perfil do usuário na sessão ou cria um novo."""
    if 'user_profile' not in session:
        session['user_profile'] = {
            'name': '',
            'age': 0,
            'preferred_genres': [],
            'ratings': {},
            'watchlist': []
        }
    return session['user_profile']

def calculate_recommendations():
    """Calcula ou recalcula as recomendações para o usuário."""
    user_profile = get_user_profile()
    if not user_profile['preferred_genres']:
        return []

    rated_movie_ids = list(user_profile['ratings'].keys())
    recommendations = []
    
    # 1. Obter todos os filmes não avaliados
    unrated_movies = [m for m in MOVIES if m['id'] not in rated_movie_ids]
    
    # 2. Se o usuário avaliou filmes, recalcular perfil de gênero
    if rated_movie_ids:
        genre_ratings = {genre: {'sum': 0, 'count': 0} for genre in MOVIE_GENRES}
        for movie_id, rating in user_profile['ratings'].items():
            movie = get_movies_by_id(movie_id)
            if movie:
                for genre in movie['genres']:
                    genre_ratings[genre]['sum'] += rating
                    genre_ratings[genre]['count'] += 1
        
        # Média de avaliação por gênero
        user_genre_profile = {
            genre: data['sum'] / data['count'] for genre, data in genre_ratings.items() if data['count'] > 0
        }
    else:
        # Se nenhuma avaliação, usar os gêneros preferidos iniciais com nota 3 (neutro)
        user_genre_profile = {genre: 3 for genre in user_profile['preferred_genres']}

    # 3. Calcular a pontuação de recomendação para cada filme não avaliado
    for movie in unrated_movies:
        score = 0
        match_reason = "Baseado em seus interesses: "
        
        # Ponderação de Similaridade de Gênero
        genre_similarity = 0
        genre_matches = []
        for genre in movie['genres']:
            if genre in user_genre_profile:
                genre_similarity += user_genre_profile[genre]
                genre_matches.append(f"• {genre}")

        if genre_matches:
            match_reason += ", ".join(genre_matches) + "."
        else:
            match_reason = "Um filme que pode ser do seu interesse."

        score += (genre_similarity / 5) * 0.7  # Pondera a similaridade do gênero (70%)
        
        # Ponderação de Popularidade
        score += (movie['popularity']) * 0.3  # Pondera a popularidade (30%)

        # Sigmoid function para converter a pontuação em uma probabilidade de gostar
        # Normaliza o score para evitar valores muito altos ou baixos
        final_score = score
        probability = 1 / (1 + math.exp(-final_score * 2))  # Multiplicador 2 para dar mais peso
        
        # A pontuação final é um valor entre 0 e 1, vamos formatar para porcentagem
        recommendations.append({
            'movie': movie,
            'probability': int(probability * 100),
            'reason': match_reason
        })

    # Ordenar por probabilidade (decrescente) e depois por popularidade
    recommendations.sort(key=lambda x: (x['probability'], x['movie']['popularity']), reverse=True)

    # Penalizar a similaridade para evitar a repetição de um mesmo tipo de filme
    # (Lógica simples: remove filmes com gêneros muito parecidos)
    if len(recommendations) > 5:
        recommendations_filtered = [recommendations[0]]
        for rec in recommendations[1:]:
            is_diverse = True
            for current_rec in recommendations_filtered:
                common_genres = set(rec['movie']['genres']) & set(current_rec['movie']['genres'])
                if len(common_genres) >= 2: # Se 2 ou mais gêneros forem iguais, considera pouco diverso
                    is_diverse = False
                    break
            if is_diverse:
                recommendations_filtered.append(rec)
        recommendations = recommendations_filtered
    
    session['recommendations'] = recommendations
    return recommendations

# --- Rotas do Flask ---

@app.route('/')
@app.route('/inicio')
def index():
    """Página de Início com o formulário de cadastro."""
    user_profile = get_user_profile()
    if user_profile['name']:
        return redirect(url_for('recommended_page'))
    
    return render_template_string(HTML_TEMPLATE, page='home', genres=MOVIE_GENRES)

@app.route('/cadastro', methods=['POST'])
def register():
    """Processa o formulário de cadastro."""
    user_profile = get_user_profile()
    user_profile['name'] = request.form.get('name', 'Usuário')
    user_profile['age'] = int(request.form.get('age', 0))
    user_profile['preferred_genres'] = request.form.getlist('genres')
    session['user_profile'] = user_profile
    calculate_recommendations()
    return redirect(url_for('recommended_page'))

@app.route('/recomendados')
def recommended_page():
    """Página de recomendações personalizadas."""
    user_profile = get_user_profile()
    if not user_profile['name']:
        return redirect(url_for('index'))
    
    recommendations = session.get('recommendations', [])
    if not recommendations:
        recommendations = calculate_recommendations()

    return render_template_string(
        HTML_TEMPLATE, 
        page='recommended', 
        user=user_profile, 
        recommendations=recommendations,
        all_movies=MOVIES
    )

@app.route('/explorar')
def explore_page():
    """Página para explorar todos os filmes com filtros e ordenação."""
    user_profile = get_user_profile()
    if not user_profile['name']:
        return redirect(url_for('index'))
    
    filtered_movies = MOVIES.copy()
    search_query = request.args.get('q', '').lower()
    genre_filter = request.args.get('genre', '')
    sort_by = request.args.get('sort_by', 'title')

    if search_query:
        filtered_movies = [m for m in filtered_movies if search_query in m['title'].lower()]
    
    if genre_filter and genre_filter != 'todos':
        filtered_movies = [m for m in filtered_movies if genre_filter in m['genres']]

    if sort_by == 'title':
        filtered_movies.sort(key=lambda x: x['title'])
    elif sort_by == 'popularity':
        filtered_movies.sort(key=lambda x: x['popularity'], reverse=True)
    elif sort_by == 'year':
        filtered_movies.sort(key=lambda x: x['year'], reverse=True)

    return render_template_string(
        HTML_TEMPLATE,
        page='explore',
        user=user_profile,
        movies=filtered_movies,
        genres=MOVIE_GENRES,
        search_query=search_query,
        genre_filter=genre_filter,
        sort_by=sort_by
    )

@app.route('/detalhes/<int:movie_id>')
def movie_details(movie_id):
    """Página de detalhes de um filme."""
    user_profile = get_user_profile()
    if not user_profile['name']:
        return redirect(url_for('index'))
    
    movie = get_movies_by_id(movie_id)
    if not movie:
        return "Filme não encontrado", 404

    # Lógica simplificada de "filmes similares" (baseada em gêneros)
    similar_movies = []
    for m in MOVIES:
        if m['id'] != movie_id:
            common_genres = set(m['genres']) & set(movie['genres'])
            if len(common_genres) > 0:
                similar_movies.append(m)
    
    # Ordena por similaridade e popularidade
    similar_movies.sort(key=lambda x: (len(set(x['genres']) & set(movie['genres'])), x['popularity']), reverse=True)

    # Garantir que não repita filmes já avaliados
    rated_movie_ids = list(user_profile['ratings'].keys())
    similar_movies = [m for m in similar_movies if m['id'] not in rated_movie_ids]

    return render_template_string(
        HTML_TEMPLATE,
        page='details',
        user=user_profile,
        movie=movie,
        similar_movies=similar_movies[:5], # Limita a 5 similares
        all_movies=MOVIES
    )

@app.route('/minha-lista')
def watchlist_page():
    """Página da lista de filmes a assistir (watchlist)."""
    user_profile = get_user_profile()
    if not user_profile['name']:
        return redirect(url_for('index'))
    
    watchlist_movies = [get_movies_by_id(mid) for mid in user_profile['watchlist']]
    watchlist_movies = [m for m in watchlist_movies if m is not None]

    return render_template_string(
        HTML_TEMPLATE, 
        page='watchlist', 
        user=user_profile,
        watchlist_movies=watchlist_movies
    )

@app.route('/minhas-notas')
def my_ratings_page():
    """Página de perfil com as notas e estatísticas por gênero."""
    user_profile = get_user_profile()
    if not user_profile['name']:
        return redirect(url_for('index'))

    # Calcula estatísticas de notas
    rated_movies = []
    genre_stats = {}
    for movie_id, rating in user_profile['ratings'].items():
        movie = get_movies_by_id(movie_id)
        if movie:
            rated_movies.append({'movie': movie, 'rating': rating})
            for genre in movie['genres']:
                if genre not in genre_stats:
                    genre_stats[genre] = {'sum': 0, 'count': 0}
                genre_stats[genre]['sum'] += rating
                genre_stats[genre]['count'] += 1

    # Calcula a média por gênero
    for genre in genre_stats:
        genre_stats[genre]['average'] = round(genre_stats[genre]['sum'] / genre_stats[genre]['count'], 2)

    return render_template_string(
        HTML_TEMPLATE, 
        page='my_ratings', 
        user=user_profile,
        rated_movies=rated_movies,
        genre_stats=genre_stats
    )

@app.route('/avaliar/<int:movie_id>/<int:rating>', methods=['POST'])
def rate_movie(movie_id, rating):
    """Endpoint para avaliar um filme (via JS fetch)."""
    user_profile = get_user_profile()
    if not 1 <= rating <= 5:
        return 'Nota inválida', 400

    user_profile['ratings'][movie_id] = rating
    session['user_profile'] = user_profile
    
    # Recalcula as recomendações após a avaliação
    calculate_recommendations()

    return 'OK'

@app.route('/add_lista/<int:movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    """Endpoint para adicionar um filme à lista (via JS fetch)."""
    user_profile = get_user_profile()
    if movie_id not in user_profile['watchlist']:
        user_profile['watchlist'].append(movie_id)
        session['user_profile'] = user_profile
        return 'Adicionado com sucesso', 200
    return 'Já está na sua lista', 409


# --- Código HTML, CSS e JS em uma única string ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Recs</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
        :root {
            --primary-color: #f7a400;
            --secondary-color: #2b2d42;
            --background-color: #1a1a2e;
            --text-color: #e0e0e0;
            --card-bg: #2d2d46;
            --star-color: #ffc107;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
            min-height: 100vh;
        }
        header {
            background: var(--secondary-color);
            padding: 1.5rem 1rem;
            text-align: center;
            border-bottom: 2px solid var(--primary-color);
        }
        nav {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 1rem;
        }
        nav a {
            color: var(--text-color);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        nav a:hover, nav a.active {
            background-color: var(--primary-color);
            color: var(--secondary-color);
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .page-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            color: var(--primary-color);
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .form-container, .card {
            background-color: var(--card-bg);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .form-container h2 {
            margin-bottom: 1.5rem;
            color: var(--primary-color);
        }
        .form-group {
            margin-bottom: 1.5rem;
        }
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        .form-group input {
            width: 100%;
            padding: 0.75rem;
            border-radius: 8px;
            border: none;
            background-color: #4a4a6b;
            color: var(--text-color);
        }
        .genre-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 0.75rem;
            margin-bottom: 1.5rem;
        }
        .genre-label {
            display: block;
            background-color: #4a4a6b;
            color: var(--text-color);
            padding: 0.75rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }
        .genre-label:hover {
            background-color: var(--primary-color);
            color: var(--secondary-color);
        }
        .genre-checkbox:checked + .genre-label {
            background-color: var(--primary-color);
            color: var(--secondary-color);
            font-weight: bold;
        }
        .genre-checkbox {
            display: none;
        }
        button {
            background-color: var(--primary-color);
            color: var(--secondary-color);
            border: none;
            padding: 1rem 2rem;
            border-radius: 9999px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        button:hover {
            opacity: 0.8;
            transform: scale(1.05);
        }
        .movie-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }
        .movie-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            position: relative;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s ease;
        }
        .movie-card:hover {
            transform: translateY(-5px);
        }
        .movie-card img {
            width: 100%;
            height: 350px;
            object-fit: cover;
            border-bottom: 2px solid var(--primary-color);
        }
        .card-content {
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }
        .card-meta {
            font-size: 0.85rem;
            color: #ccc;
            margin-bottom: 1rem;
        }
        .card-probability {
            background: var(--primary-color);
            color: var(--secondary-color);
            font-size: 1.5rem;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            position: absolute;
            top: 1rem;
            right: 1rem;
        }
        .card-reason {
            font-style: italic;
            font-size: 0.9rem;
            color: #aaa;
            margin-bottom: 1rem;
        }
        .rating-stars {
            display: flex;
            justify-content: center;
            gap: 0.25rem;
            margin-top: auto;
            align-items: center;
        }
        .rating-stars .star-label {
            font-size: 1.5rem;
            cursor: pointer;
            transition: transform 0.2s ease;
            color: #888;
        }
        .rating-stars .star-label:hover,
        .rating-stars .star-label.hover,
        .rating-stars .star-label.selected {
            color: var(--star-color);
            transform: scale(1.1);
        }
        .star-input {
            display: none;
        }
        .btn-link {
            text-decoration: none;
            color: var(--primary-color);
            font-weight: 600;
            display: inline-block;
            margin-top: 1rem;
            text-align: center;
        }
        .watchlist-btn {
            background-color: var(--primary-color);
            color: var(--secondary-color);
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .watchlist-btn:hover {
            background-color: #ffd700;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
        }
        .stat-card {
            background-color: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
        }
        .stat-card h3 {
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            color: var(--primary-color);
        }
        .stat-card p {
            font-size: 1.5rem;
            font-weight: bold;
        }
        .rating-list {
            list-style: none;
            padding: 0;
        }
        .rating-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background-color: var(--card-bg);
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .rating-item span {
            font-weight: bold;
        }
        .filter-sort-bar {
            background-color: var(--card-bg);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .filter-sort-bar input, .filter-sort-bar select {
            padding: 0.75rem;
            border-radius: 8px;
            border: none;
            background-color: #4a4a6b;
            color: var(--text-color);
            width: 100%;
        }
        @media (min-width: 768px) {
            .filter-sort-bar {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }
            .filter-sort-bar > * {
                flex: 1;
            }
        }
        .movie-details-poster {
            max-width: 400px;
            margin: 0 auto 2rem;
            border-radius: 12px;
            border: 3px solid var(--primary-color);
        }
        .movie-details-content {
            text-align: center;
        }
        .movie-details-content h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .movie-details-content p {
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 1.5rem;
        }
        .similar-movies-section {
            margin-top: 3rem;
        }
        .similar-movies-section h2 {
            text-align: center;
            margin-bottom: 2rem;
            color: var(--primary-color);
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background-color: var(--card-bg);
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
        }
        .modal-close {
            color: var(--text-color);
            float: right;
            font-size: 28px;
            font-weight: bold;
        }
        .modal-close:hover, .modal-close:focus {
            color: var(--primary-color);
            text-decoration: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <header>
        <h1 style="color: var(--text-color);">Movie Recs</h1>
        {% if user.name %}
            <nav>
                <a href="{{ url_for('recommended_page') }}" class="{% if page == 'recommended' %}active{% endif %}">Recomendados</a>
                <a href="{{ url_for('explore_page') }}" class="{% if page == 'explore' %}active{% endif %}">Explorar</a>
                <a href="{{ url_for('watchlist_page') }}" class="{% if page == 'watchlist' %}active{% endif %}">Minha Lista</a>
                <a href="{{ url_for('my_ratings_page') }}" class="{% if page == 'my_ratings' %}active{% endif %}">Minhas Notas</a>
                <a href="{{ url_for('index') }}" onclick="logout()">Sair</a>
            </nav>
        {% endif %}
    </header>

    <main class="container">
        {% if page == 'home' %}
            <div class="form-container">
                <h2>Bem-vindo(a) ao Movie Recs!</h2>
                <p>Para começar, nos diga um pouco sobre você.</p>
                <form action="{{ url_for('register') }}" method="post">
                    <div class="form-group">
                        <label for="name">Seu Nome:</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="age">Sua Idade:</label>
                        <input type="number" id="age" name="age" min="1" required>
                    </div>
                    <div class="form-group">
                        <label>Gêneros de Filme Favoritos:</label>
                        <div class="genre-grid">
                            {% for genre in genres %}
                                <div>
                                    <input type="checkbox" id="genre-{{ genre }}" name="genres" value="{{ genre }}" class="genre-checkbox">
                                    <label for="genre-{{ genre }}" class="genre-label">{{ genre }}</label>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                    <button type="submit">Cadastrar e Começar</button>
                </form>
            </div>
        {% elif page == 'recommended' %}
            <h2 class="page-title">Recomendado para {{ user.name }}</h2>
            <div class="movie-grid">
                {% for rec in recommendations %}
                    <div class="movie-card">
                        <img src="{{ rec.movie.poster_url }}" alt="Poster do filme {{ rec.movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/500x750?text=Sem+Poster';">
                        <div class="card-content">
                            <span class="card-probability">{{ rec.probability }}%</span>
                            <h3 class="card-title">{{ rec.movie.title }}</h3>
                            <p class="card-meta">{{ rec.movie.year }} | {{ ', '.join(rec.movie.genres) }}</p>
                            <p class="card-reason">{{ rec.reason }}</p>
                            <div class="rating-stars" data-movie-id="{{ rec.movie.id }}">
                                {% for i in range(1, 6) %}
                                    <label class="star-label" for="star-{{ rec.movie.id }}-{{ i }}">&#9733;</label>
                                    <input type="radio" id="star-{{ rec.movie.id }}-{{ i }}" name="rating-{{ rec.movie.id }}" value="{{ i }}" class="star-input" onclick="rateMovie({{ rec.movie.id }}, {{ i }})">
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% elif page == 'explore' %}
            <h2 class="page-title">Explorar Filmes</h2>
            <div class="filter-sort-bar">
                <form action="{{ url_for('explore_page') }}" method="get" style="display: flex; gap: 1rem; width: 100%;">
                    <input type="text" name="q" placeholder="Buscar por título..." value="{{ search_query or '' }}">
                    <select name="genre">
                        <option value="todos">Todos os Gêneros</option>
                        {% for genre in genres %}
                            <option value="{{ genre }}" {% if genre == genre_filter %}selected{% endif %}>{{ genre }}</option>
                        {% endfor %}
                    </select>
                    <select name="sort_by">
                        <option value="title" {% if sort_by == 'title' %}selected{% endif %}>Título (A-Z)</option>
                        <option value="popularity" {% if sort_by == 'popularity' %}selected{% endif %}>Popularidade</option>
                        <option value="year" {% if sort_by == 'year' %}selected{% endif %}>Ano (Recente)</option>
                    </select>
                    <button type="submit">Buscar/Filtrar</button>
                </form>
            </div>
            <div class="movie-grid">
                {% for movie in movies %}
                    <a href="{{ url_for('movie_details', movie_id=movie.id) }}" class="movie-card" style="text-decoration:none;">
                        <img src="{{ movie.poster_url }}" alt="Poster do filme {{ movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/500x750?text=Sem+Poster';">
                        <div class="card-content">
                            <h3 class="card-title">{{ movie.title }}</h3>
                            <p class="card-meta">{{ movie.year }} | {{ ', '.join(movie.genres) }}</p>
                        </div>
                    </a>
                {% endfor %}
            </div>
        {% elif page == 'details' %}
            <div class="movie-details-content">
                <img src="{{ movie.poster_url }}" alt="Poster do filme {{ movie.title }}" class="movie-details-poster" onerror="this.onerror=null;this.src='https://placehold.co/500x750?text=Sem+Poster';">
                <h1>{{ movie.title }}</h1>
                <p class="card-meta">{{ movie.year }} | {{ ', '.join(movie.genres) }}</p>
                <p>{{ movie.plot }}</p>
                <button class="watchlist-btn" onclick="addToWatchlist({{ movie.id }})">Adicionar à Minha Lista</button>
                <div class="rating-stars" data-movie-id="{{ movie.id }}">
                    <p style="margin-top:1rem; font-weight:bold; color:var(--text-color);">Sua avaliação:</p>
                    {% for i in range(1, 6) %}
                        <label class="star-label" for="star-{{ movie.id }}-{{ i }}">&#9733;</label>
                        <input type="radio" id="star-{{ movie.id }}-{{ i }}" name="rating-{{ movie.id }}" value="{{ i }}" class="star-input" onclick="rateMovie({{ movie.id }}, {{ i }})" {% if user.ratings.get(movie.id) == i %}checked{% endif %}>
                    {% endfor %}
                </div>
            </div>
            {% if similar_movies %}
            <div class="similar-movies-section">
                <h2>Filmes Similares</h2>
                <div class="movie-grid">
                    {% for sim_movie in similar_movies %}
                        <a href="{{ url_for('movie_details', movie_id=sim_movie.id) }}" class="movie-card" style="text-decoration:none;">
                            <img src="{{ sim_movie.poster_url }}" alt="Poster do filme {{ sim_movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/500x750?text=Sem+Poster';">
                            <div class="card-content">
                                <h3 class="card-title">{{ sim_movie.title }}</h3>
                                <p class="card-meta">{{ sim_movie.year }}</p>
                            </div>
                        </a>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
        {% elif page == 'watchlist' %}
            <h2 class="page-title">Minha Lista de Filmes</h2>
            {% if watchlist_movies %}
                <div class="movie-grid">
                    {% for movie in watchlist_movies %}
                        <a href="{{ url_for('movie_details', movie_id=movie.id) }}" class="movie-card" style="text-decoration:none;">
                            <img src="{{ movie.poster_url }}" alt="Poster do filme {{ movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/500x750?text=Sem+Poster';">
                            <div class="card-content">
                                <h3 class="card-title">{{ movie.title }}</h3>
                                <p class="card-meta">{{ movie.year }}</p>
                            </div>
                        </a>
                    {% endfor %}
                </div>
            {% else %}
                <p style="text-align: center; font-size: 1.2rem;">Sua lista de filmes está vazia. Adicione alguns filmes da página <a href="{{ url_for('explore_page') }}" style="color:var(--primary-color);">Explorar</a>.</p>
            {% endif %}
        {% elif page == 'my_ratings' %}
            <h2 class="page-title">Minhas Notas e Gêneros Favoritos</h2>
            {% if user.ratings %}
                <div class="stats-grid">
                    {% for genre, stats in genre_stats.items() %}
                        <div class="stat-card">
                            <h3>{{ genre }}</h3>
                            <p>Média: {{ stats.average }}</p>
                            <p>Notas: {{ stats.count }}</p>
                        </div>
                    {% endfor %}
                </div>
                <h3 style="margin-top:2rem; text-align:center; color: var(--primary-color);">Filmes que Você Avaliou</h3>
                <ul class="rating-list">
                    {% for item in rated_movies %}
                        <li class="rating-item">
                            <span>{{ item.movie.title }}</span>
                            <span>Nota: {{ item.rating }}/5</span>
                        </li>
                    {% endfor %}
                </ul>
            {% else %}
                <p style="text-align: center; font-size: 1.2rem;">Você ainda não avaliou nenhum filme. Suas recomendações ficarão mais precisas depois de avaliar alguns!</p>
            {% endif %}
        {% endif %}
    </main>

    <div id="message-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close">&times;</span>
            <p id="modal-text"></p>
        </div>
    </div>

    <script>
        // Função para mostrar um modal de mensagem
        function showMessage(text) {
            const modal = document.getElementById('message-modal');
            const modalText = document.getElementById('modal-text');
            modalText.textContent = text;
            modal.style.display = 'flex';
        }
        
        // Fechar o modal
        document.querySelector('.modal-close').onclick = function() {
            document.getElementById('message-modal').style.display = 'none';
        }
        window.onclick = function(event) {
            if (event.target == document.getElementById('message-modal')) {
                document.getElementById('message-modal').style.display = 'none';
            }
        }

        // Lógica para enviar a avaliação via AJAX/Fetch
        async function rateMovie(movieId, rating) {
            const response = await fetch('/avaliar/' + movieId + '/' + rating, {
                method: 'POST'
            });
            if (response.ok) {
                showMessage('Obrigado pela sua avaliação! Suas recomendações foram atualizadas.');
                // Recarrega a página para mostrar as novas recomendações
                // setTimeout(() => { window.location.reload(); }, 1500); 
            } else {
                showMessage('Ocorreu um erro ao registrar sua avaliação.');
            }
        }
        
        // Lógica para adicionar à lista
        async function addToWatchlist(movieId) {
            const response = await fetch('/add_lista/' + movieId, {
                method: 'POST'
            });
            const text = await response.text();
            showMessage(text);
        }

        function logout() {
            sessionStorage.clear(); // Limpa dados da sessão do navegador
        }
        
        // Lógica para as estrelas
        document.querySelectorAll('.rating-stars').forEach(container => {
            const stars = container.querySelectorAll('.star-label');
            stars.forEach((star, index) => {
                star.addEventListener('mouseover', () => {
                    stars.forEach((s, sIndex) => {
                        if (sIndex <= index) {
                            s.classList.add('hover');
                        } else {
                            s.classList.remove('hover');
                        }
                    });
                });
                star.addEventListener('mouseout', () => {
                    stars.forEach(s => s.classList.remove('hover'));
                });
            });
        });

    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
