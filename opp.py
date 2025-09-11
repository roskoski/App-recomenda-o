import json
import math
import random
from flask import Flask, render_template_string, request, redirect, url_for, session

# --- Configurações Iniciais ---
app = Flask(__name__)
app.secret_key = 'super-secret-key-para-sessao'

# --- Dados do Aplicativo (simulando um banco de dados em memória) ---

GENRES = [
    "Ação", "Aventura", "Comédia", "Drama", "Ficção Científica",
    "Fantasia", "Suspense", "Terror", "Animação", "Documentário",
    "Romance", "Crime", "Mistério", "Musical", "História"
]

MOVIES = {
    1: {
        "title": "A Origem",
        "poster_url": "https://m.media-amazon.com/images/I/91t79wB58TL._AC_SL1500_.jpg",
        "genres": ["Ação", "Ficção Científica", "Suspense"],
        "description": "Dom Cobb é um ladrão com a rara habilidade de invadir os sonhos das pessoas e roubar seus segredos do subconsciente. Ele recebe uma oferta para plantar uma ideia em vez de roubá-la.",
        "popularity": 0.95
    },
    2: {
        "title": "Interestelar",
        "poster_url": "https://m.media-amazon.com/images/I/914Tz2i0GEL._AC_SL1500_.jpg",
        "genres": ["Ficção Científica", "Aventura", "Drama"],
        "description": "Em um futuro distópico, a humanidade luta para sobreviver. Um grupo de exploradores viaja através de um buraco de minhoca no espaço em uma tentativa de garantir a sobrevivência da raça humana.",
        "popularity": 0.92
    },
    3: {
        "title": "O Poderoso Chefão",
        "poster_url": "https://m.media-amazon.com/images/I/81+S12mH8wL._AC_SL1500_.jpg",
        "genres": ["Crime", "Drama"],
        "description": "O patriarca da família do crime Corleone transfere o controle de seu império clandestino para seu filho relutante.",
        "popularity": 0.98
    },
    4: {
        "title": "A Rede Social",
        "poster_url": "https://m.media-amazon.com/images/I/719h+n1P46L._AC_SL1500_.jpg",
        "genres": ["Drama", "História"],
        "description": "A história de como o Facebook foi criado e a disputa legal que se seguiu entre Mark Zuckerberg e seus antigos parceiros de negócio.",
        "popularity": 0.88
    },
    5: {
        "title": "Pulp Fiction",
        "poster_url": "https://m.media-amazon.com/images/I/715b+a1tU3L._AC_SL1500_.jpg",
        "genres": ["Crime", "Drama"],
        "description": "As vidas de dois assassinos de aluguel, um boxeador, a esposa de um gangster e um par de assaltantes de restaurante se entrelaçam em quatro contos de violência e redenção.",
        "popularity": 0.94
    },
    6: {
        "title": "E.T. O Extraterrestre",
        "poster_url": "https://m.media-amazon.com/images/I/61G+4t-f05L._AC_SL1200_.jpg",
        "genres": ["Ficção Científica", "Fantasia"],
        "description": "Uma criatura alienígena é acidentalmente deixada para trás na Terra e faz amizade com um garoto solitário.",
        "popularity": 0.85
    },
    7: {
        "title": "Os Incríveis",
        "poster_url": "https://m.media-amazon.com/images/I/81577dY1cIL._AC_SL1500_.jpg",
        "genres": ["Animação", "Ação", "Aventura"],
        "description": "Uma família de super-heróis tenta viver uma vida suburbana normal, mas são forçados a voltar à ação para salvar o mundo.",
        "popularity": 0.90
    },
    8: {
        "title": "A Viagem de Chihiro",
        "poster_url": "https://m.media-amazon.com/images/I/8140JkK9b6L._AC_SL1500_.jpg",
        "genres": ["Animação", "Fantasia"],
        "description": "Uma garota de 10 anos se perde em um mundo de espíritos, deuses e bruxas, e deve trabalhar em uma casa de banho para sobreviver e encontrar uma maneira de voltar para casa.",
        "popularity": 0.91
    },
    9: {
        "title": "O Senhor dos Anéis: A Sociedade do Anel",
        "poster_url": "https://m.media-amazon.com/images/I/71uIqYf75EL._AC_SL1494_.jpg",
        "genres": ["Aventura", "Fantasia"],
        "description": "Um jovem hobbit herda um anel e embarca em uma jornada épica para destruí-lo e salvar a Terra Média do Senhor das Trevas.",
        "popularity": 0.96
    },
    10: {
        "title": "O Fabuloso Destino de Amélie Poulain",
        "poster_url": "https://m.media-amazon.com/images/I/811F3h3h5WL._AC_SL1500_.jpg",
        "genres": ["Comédia", "Romance"],
        "description": "Amélie, uma garçonete inocente e ingênua em Paris, decide mudar a vida das pessoas ao seu redor para melhor.",
        "popularity": 0.87
    },
    11: {
        "title": "Parasita",
        "poster_url": "https://m.media-amazon.com/images/I/71Y8+J0t9pL._AC_SL1500_.jpg",
        "genres": ["Drama", "Suspense", "Comédia"],
        "description": "A família Ki-taek, desempregada, se infiltra na rica família Park e um incidente inesperado ameaça destruir sua nova vida.",
        "popularity": 0.93
    },
    12: {
        "title": "Whiplash: Em Busca da Perfeição",
        "poster_url": "https://m.media-amazon.com/images/I/71jQx54g2SL._AC_SL1500_.jpg",
        "genres": ["Drama", "Musical"],
        "description": "Um jovem baterista talentoso é levado ao limite por seu professor de música obsessivo em uma das melhores escolas de música do país.",
        "popularity": 0.89
    },
    13: {
        "title": "O Iluminado",
        "poster_url": "https://m.media-amazon.com/images/I/910q32n8q+L._AC_SL1500_.jpg",
        "genres": ["Terror", "Suspense"],
        "description": "Um escritor e sua família se tornam os zeladores de um hotel isolado durante o inverno. Ele é gradualmente consumido pela loucura enquanto forças sobrenaturais se manifestam.",
        "popularity": 0.91
    },
    14: {
        "title": "O Resgate do Soldado Ryan",
        "poster_url": "https://m.media-amazon.com/images/I/918u-f+zI7L._AC_SL1500_.jpg",
        "genres": ["Ação", "Drama", "Guerra"],
        "description": "Em meio à invasão da Normandia durante a Segunda Guerra Mundial, um esquadrão de soldados é enviado em uma missão para resgatar um paraquedista.",
        "popularity": 0.90
    },
    15: {
        "title": "Toy Story",
        "poster_url": "https://m.media-amazon.com/images/I/71gVl1H2gBL._AC_SL1500_.jpg",
        "genres": ["Animação", "Comédia"],
        "description": "Um boneco de cowboy é aterrorizado por um novo e moderno brinquedo espacial que se torna o favorito de seu dono.",
        "popularity": 0.88
    },
    16: {
        "title": "Matrix",
        "poster_url": "https://m.media-amazon.com/images/I/81+m42B9xPL._AC_SL1500_.jpg",
        "genres": ["Ação", "Ficção Científica"],
        "description": "Um programador de computador descobre que a realidade que conhece é uma simulação de computador criada por máquinas inteligentes.",
        "popularity": 0.94
    }
}

# --- Lógica de Recomendação ---

def sigmoid(x):
    """Função sigmoide para converter uma pontuação em probabilidade."""
    return 1 / (1 + math.exp(-x))

def calculate_user_profile(user_ratings):
    """Calcula as preferências de gênero do usuário com base em suas avaliações."""
    user_profile = {genre: 0 for genre in GENRES}
    if not user_ratings:
        return user_profile

    total_ratings = sum(1 for _, rating in user_ratings.items() if rating > 0)
    if total_ratings == 0:
        return user_profile

    for movie_id, rating in user_ratings.items():
        movie = MOVIES.get(int(movie_id))
        if movie:
            for genre in movie["genres"]:
                # Pondera o gênero com base na avaliação (1-5)
                # Aumenta a pontuação para avaliações altas, diminui para baixas
                user_profile[genre] += (rating - 3) / 2

    # Normaliza o perfil do usuário para evitar pontuações extremas
    max_val = max(abs(v) for v in user_profile.values()) or 1
    for genre in user_profile:
        user_profile[genre] /= max_val

    return user_profile

def get_recommendations(user_profile, rated_movies_ids):
    """Gera recomendações com base no perfil do usuário."""
    recommendations = []
    
    # 1. Encontra filmes que não foram avaliados
    unrated_movies = {mid: movie for mid, movie in MOVIES.items() if mid not in rated_movies_ids}
    
    # 2. Calcula a pontuação de similaridade para cada filme não avaliado
    for movie_id, movie in unrated_movies.items():
        score = 0
        for genre in movie["genres"]:
            score += user_profile.get(genre, 0)
        
        # Adiciona um fator de popularidade para dar um "empurrão" em filmes populares
        score += movie["popularity"] * 0.5
        
        # Penaliza filmes com gêneros muito repetidos no perfil do usuário
        # Isso promove a diversidade
        if len(movie["genres"]) > 1:
            score -= (len(movie["genres"]) - 1) * 0.1
        
        # Converte a pontuação bruta em uma probabilidade %
        probability = round(sigmoid(score) * 100)
        
        # Determina o motivo da recomendação
        reasons = [f"Combina com seu interesse em {genre}" for genre, pref in user_profile.items() if pref > 0.1]
        reason = "Baseado em seus gostos" if not reasons else random.choice(reasons)
        
        recommendations.append({
            "id": movie_id,
            "title": movie["title"],
            "poster_url": movie["poster_url"],
            "probability": probability,
            "reason": reason,
            "description": movie["description"],
            "genres": movie["genres"]
        })

    # 3. Ordena por probabilidade e escolhe os 10 melhores
    recommendations.sort(key=lambda x: x["probability"], reverse=True)
    return recommendations[:10]

# --- Templates HTML e CSS embutidos como strings ---

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    body {
        font-family: 'Inter', sans-serif;
        background-color: #121212;
        color: #e0e0e0;
        margin: 0;
        padding: 0;
        line-height: 1.6;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    .header {
        background-color: #1f1f1f;
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .header h1 {
        margin: 0;
        font-size: 1.8rem;
    }
    .nav a {
        color: #e0e0e0;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: background-color 0.3s, color 0.3s;
    }
    .nav a:hover {
        background-color: #333;
        color: #fff;
    }
    .content {
        background-color: #1f1f1f;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .form-card {
        background-color: #2a2a2a;
        padding: 2rem;
        border-radius: 12px;
        max-width: 500px;
        margin: 2rem auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    h2 {
        color: #fff;
        font-weight: 600;
        margin-top: 0;
    }
    .genre-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 0.75rem;
    }
    .genre-item {
        background-color: #333;
        color: #fff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        cursor: pointer;
        transition: background-color 0.3s;
        border: 2px solid transparent;
    }
    .genre-item:hover {
        background-color: #555;
    }
    .genre-item.selected {
        background-color: #007bff;
        border-color: #007bff;
    }
    .btn {
        background-color: #007bff;
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
    }
    .btn:hover {
        background-color: #0056b3;
    }
    .input-group {
        margin-bottom: 1rem;
    }
    .input-group label {
        display: block;
        margin-bottom: 0.5rem;
    }
    .input-group input {
        width: 100%;
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #444;
        background-color: #333;
        color: #e0e0e0;
    }
    .movie-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    .movie-card {
        background-color: #2a2a2a;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s, box-shadow 0.2s;
        cursor: pointer;
        text-decoration: none;
        color: #e0e0e0;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    .movie-card img {
        width: 100%;
        height: 300px;
        object-fit: cover;
    }
    .movie-info {
        padding: 1rem;
    }
    .movie-info h3 {
        margin-top: 0;
        font-size: 1.2rem;
        height: 3rem;
        overflow: hidden;
    }
    .tag {
        background-color: #444;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .rating-buttons button {
        background-color: #333;
        border: 1px solid #444;
        color: #e0e0e0;
        padding: 0.5rem;
        border-radius: 8px;
        margin-right: 0.25rem;
        cursor: pointer;
        transition: background-color 0.2s, transform 0.1s;
    }
    .rating-buttons button:hover {
        background-color: #555;
        transform: scale(1.05);
    }
    .rating-buttons .selected {
        background-color: #007bff;
        border-color: #007bff;
    }
    .details-page {
        display: flex;
        gap: 2rem;
    }
    .details-page img {
        width: 300px;
        height: auto;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    .movie-details {
        flex: 1;
    }
    .movie-details h2 {
        font-size: 2.5rem;
        margin-top: 0;
        color: #fff;
    }
    .movie-details p {
        color: #ccc;
    }
    .profile-scores p {
        background-color: #2a2a2a;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    @media (max-width: 768px) {
        .header {
            flex-direction: column;
            align-items: flex-start;
        }
        .nav {
            margin-top: 1rem;
        }
        .details-page {
            flex-direction: column;
        }
        .details-page img {
            width: 100%;
        }
    }
</style>
"""

BASE_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cine Sugestão - {{ title }}</title>
    {{ css | safe }}
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>Cine Sugestão</h1>
            <nav class="nav">
                <a href="{{ url_for('recommended') }}">Recomendados</a>
                <a href="{{ url_for('explore') }}">Explorar</a>
                <a href="{{ url_for('watchlist') }}">Minha Lista</a>
                <a href="{{ url_for('my_scores') }}">Minhas Notas</a>
                <a href="{{ url_for('search') }}">Busca</a>
            </nav>
        </header>
        <main class="content">
            {% block content %}{% endblock %}
        </main>
    </div>
</body>
</html>
"""

HOME_HTML = """
{% extends "base.html" %}
{% block content %}
<div class="form-card">
    <h2>Bem-vindo(a) ao Cine Sugestão!</h2>
    <p>Para começar, nos conte um pouco sobre você e seus gêneros favoritos. Isso nos ajudará a encontrar os filmes perfeitos!</p>
    <form action="{{ url_for('register') }}" method="post" id="register-form">
        <div class="input-group">
            <label for="name">Nome:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="input-group">
            <label for="age">Idade:</label>
            <input type="number" id="age" name="age" required>
        </div>
        <div class="input-group">
            <label>Escolha 3 ou mais gêneros:</label>
            <div class="genre-grid">
                {% for genre in genres %}
                <div class="genre-item" data-genre="{{ genre }}">{{ genre }}</div>
                {% endfor %}
            </div>
            <input type="hidden" id="selected-genres" name="genres">
        </div>
        <button type="submit" class="btn">Cadastrar e Ver Recomendações</button>
    </form>
</div>
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const items = document.querySelectorAll('.genre-item');
        const hiddenInput = document.getElementById('selected-genres');
        let selected = new Set();
        items.forEach(item => {
            item.addEventListener('click', () => {
                const genre = item.dataset.genre;
                if (selected.has(genre)) {
                    selected.delete(genre);
                    item.classList.remove('selected');
                } else {
                    selected.add(genre);
                    item.classList.add('selected');
                }
                hiddenInput.value = JSON.stringify(Array.from(selected));
            });
        });

        document.getElementById('register-form').addEventListener('submit', (e) => {
            if (selected.size < 3) {
                alert('Por favor, selecione pelo menos 3 gêneros.');
                e.preventDefault();
            }
        });
    });
</script>
{% endblock %}
"""

RECOMMENDED_HTML = """
{% extends "base.html" %}
{% block content %}
    <h2>Filmes Recomendados para Você</h2>
    <p>Olá, {{ session['user_name'] }}! Aqui estão os filmes que achamos que você vai gostar, baseados no seu perfil e nas suas avaliações.</p>
    <div class="movie-card-grid">
        {% for movie in recommendations %}
            <div class="movie-card">
                <a href="{{ url_for('movie_details', movie_id=movie.id) }}">
                    <img src="{{ movie.poster_url }}" alt="Poster de {{ movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/200x300/1e1e1e/888?text=Sem+Poster';">
                </a>
                <div class="movie-info">
                    <h3>{{ movie.title }}</h3>
                    <p class="tag-row">
                        <span class="tag">Chance: {{ movie.probability }}%</span>
                    </p>
                    <p>{{ movie.reason }}</p>
                    <div class="rating-buttons">
                        {% for i in range(1, 6) %}
                            <button onclick="rateMovie({{ movie.id }}, {{ i }})">{{ i }}</button>
                        {% endfor %}
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
    <script>
        function rateMovie(movieId, rating) {
            fetch(`/rate/${movieId}/${rating}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert('Erro ao registrar sua avaliação. Tente novamente.');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert('Erro de conexão.');
                });
        }
    </script>
{% endblock %}
"""

EXPLORE_HTML = """
{% extends "base.html" %}
{% block content %}
    <h2>Explorar Filmes</h2>
    <p>Use os filtros para encontrar novos filmes. Você pode avaliá-los aqui mesmo!</p>
    <form id="explore-form">
        <div class="input-group">
            <label for="genre-filter">Filtrar por Gênero:</label>
            <select id="genre-filter" name="genre" onchange="this.form.submit()">
                <option value="">Todos</option>
                {% for genre in genres %}
                    <option value="{{ genre }}" {% if genre == selected_genre %}selected{% endif %}>{{ genre }}</option>
                {% endfor %}
            </select>
        </div>
    </form>
    <div class="movie-card-grid">
        {% for movie in movies %}
            <div class="movie-card">
                <a href="{{ url_for('movie_details', movie_id=movie.id) }}">
                    <img src="{{ movie.poster_url }}" alt="Poster de {{ movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/200x300/1e1e1e/888?text=Sem+Poster';">
                </a>
                <div class="movie-info">
                    <h3>{{ movie.title }}</h3>
                    <div class="rating-buttons">
                        {% for i in range(1, 6) %}
                            <button onclick="rateMovie({{ movie.id }}, {{ i }})">{{ i }}</button>
                        {% endfor %}
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
    <script>
        function rateMovie(movieId, rating) {
            fetch(`/rate/${movieId}/${rating}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert('Erro ao registrar sua avaliação. Tente novamente.');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert('Erro de conexão.');
                });
        }
    </script>
{% endblock %}
"""

DETAILS_HTML = """
{% extends "base.html" %}
{% block content %}
    {% if movie %}
        <div class="details-page">
            <img src="{{ movie.poster_url }}" alt="Poster de {{ movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/300x450/1e1e1e/888?text=Sem+Poster';">
            <div class="movie-details">
                <h2>{{ movie.title }}</h2>
                <p><strong>Gêneros:</strong> {{ movie.genres | join(', ') }}</p>
                <p><strong>Sinopse:</strong> {{ movie.description }}</p>
                <p><strong>Sua Nota:</strong> {{ rating }} de 5 estrelas</p>
                <div class="rating-buttons">
                    {% for i in range(1, 6) %}
                        <button onclick="rateMovie({{ movie.id }}, {{ i }})" class="{% if i == rating %}selected{% endif %}">{{ i }}</button>
                    {% endfor %}
                </div>
                <h3 style="margin-top: 2rem;">Filmes Similares</h3>
                <div class="movie-card-grid">
                    {% for similar in similar_movies %}
                        <div class="movie-card">
                            <a href="{{ url_for('movie_details', movie_id=similar.id) }}">
                                <img src="{{ similar.poster_url }}" alt="Poster de {{ similar.title }}" onerror="this.onerror=null;this.src='https://placehold.co/200x300/1e1e1e/888?text=Sem+Poster';">
                            </a>
                            <div class="movie-info">
                                <h3>{{ similar.title }}</h3>
                                <p class="tag-row"><span class="tag">Similaridade: {{ similar.probability }}%</span></p>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    {% else %}
        <h2>Filme não encontrado.</h2>
    {% endif %}
    <script>
        function rateMovie(movieId, rating) {
            fetch(`/rate/${movieId}/${rating}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert('Erro ao registrar sua avaliação. Tente novamente.');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert('Erro de conexão.');
                });
        }
    </script>
{% endblock %}
"""

WATCHLIST_HTML = """
{% extends "base.html" %}
{% block content %}
    <h2>Minha Lista (Watchlist)</h2>
    <p>Aqui estão os filmes que você adicionou à sua lista para assistir mais tarde.</p>
    {% if watchlist %}
        <div class="movie-card-grid">
            {% for movie in watchlist %}
                <div class="movie-card">
                    <a href="{{ url_for('movie_details', movie_id=movie.id) }}">
                        <img src="{{ movie.poster_url }}" alt="Poster de {{ movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/200x300/1e1e1e/888?text=Sem+Poster';">
                    </a>
                    <div class="movie-info">
                        <h3>{{ movie.title }}</h3>
                        <p>Avalie este filme:</p>
                        <div class="rating-buttons">
                            {% for i in range(1, 6) %}
                                <button onclick="rateMovie({{ movie.id }}, {{ i }})">{{ i }}</button>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p>Sua lista está vazia. Adicione filmes para assistir mais tarde na página de detalhes!</p>
    {% endif %}
    <script>
        function rateMovie(movieId, rating) {
            fetch(`/rate/${movieId}/${rating}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert('Erro ao registrar sua avaliação. Tente novamente.');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert('Erro de conexão.');
                });
        }
    </script>
{% endblock %}
"""

MY_SCORES_HTML = """
{% extends "base.html" %}
{% block content %}
    <h2>Minhas Notas e Perfil de Gêneros</h2>
    <p>Este é o seu perfil de gostos. As pontuações abaixo refletem sua afinidade com cada gênero, baseada nas suas avaliações.</p>
    <div class="profile-scores">
        {% for genre, score in scores.items() %}
            <p><strong>{{ genre }}:</strong> {{ '%.2f' % (score * 100) }}%</p>
        {% endfor %}
    </div>
{% endblock %}
"""

SEARCH_HTML = """
{% extends "base.html" %}
{% block content %}
    <h2>Busca de Filmes</h2>
    <form action="{{ url_for('search') }}" method="get">
        <div class="input-group">
            <label for="query">Buscar por título:</label>
            <input type="text" id="query" name="query" value="{{ query }}" required>
            <button type="submit" class="btn">Buscar</button>
        </div>
    </form>
    {% if movies %}
        <div class="movie-card-grid">
            {% for movie in movies %}
                <div class="movie-card">
                    <a href="{{ url_for('movie_details', movie_id=movie.id) }}">
                        <img src="{{ movie.poster_url }}" alt="Poster de {{ movie.title }}" onerror="this.onerror=null;this.src='https://placehold.co/200x300/1e1e1e/888?text=Sem+Poster';">
                    </a>
                    <div class="movie-info">
                        <h3>{{ movie.title }}</h3>
                        <p>Avalie este filme:</p>
                        <div class="rating-buttons">
                            {% for i in range(1, 6) %}
                                <button onclick="rateMovie({{ movie.id }}, {{ i }})">{{ i }}</button>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% elif query %}
        <p>Nenhum filme encontrado para "{{ query }}".</p>
    {% endif %}
    <script>
        function rateMovie(movieId, rating) {
            fetch(`/rate/${movieId}/${rating}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert('Erro ao registrar sua avaliação. Tente novamente.');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert('Erro de conexão.');
                });
        }
    </script>
{% endblock %}
"""

# --- Rotas da Aplicação ---

@app.route('/')
def home():
    if 'user_name' in session:
        return redirect(url_for('recommended'))
    return render_template_string(BASE_HTML + HOME_HTML, title="Início", css=CSS, genres=GENRES)

@app.route('/register', methods=['POST'])
def register():
    session['user_name'] = request.form['name']
    session['user_age'] = request.form['age']
    selected_genres = json.loads(request.form['genres'])
    session['initial_genres'] = selected_genres
    session['ratings'] = {}
    session['watchlist'] = []
    
    # Cria o perfil inicial do usuário com base nos gêneros selecionados
    user_profile = {genre: 0 for genre in GENRES}
    for genre in selected_genres:
        user_profile[genre] = 1
    session['user_profile'] = user_profile

    return redirect(url_for('recommended'))

@app.route('/recommended')
def recommended():
    if 'user_name' not in session:
        return redirect(url_for('home'))

    user_profile = session.get('user_profile', {})
    rated_movies_ids = {int(mid) for mid in session.get('ratings', {})}

    recommendations = get_recommendations(user_profile, rated_movies_ids)
    
    return render_template_string(
        BASE_HTML + RECOMMENDED_HTML,
        title="Recomendados",
        css=CSS,
        recommendations=recommendations
    )

@app.route('/explore')
def explore():
    if 'user_name' not in session:
        return redirect(url_for('home'))

    selected_genre = request.args.get('genre', '')
    
    movies_to_show = MOVIES
    if selected_genre:
        movies_to_show = {mid: movie for mid, movie in MOVIES.items() if selected_genre in movie["genres"]}

    explore_movies = sorted(list(movies_to_show.items()), key=lambda x: x[1]['popularity'], reverse=True)
    
    return render_template_string(
        BASE_HTML + EXPLORE_HTML,
        title="Explorar",
        css=CSS,
        genres=GENRES,
        movies=[{"id": mid, **movie} for mid, movie in explore_movies],
        selected_genre=selected_genre
    )

@app.route('/details/<int:movie_id>')
def movie_details(movie_id):
    if 'user_name' not in session:
        return redirect(url_for('home'))

    movie = MOVIES.get(movie_id)
    if not movie:
        return render_template_string(BASE_HTML + "<h2>Filme não encontrado.</h2>", title="Detalhes do Filme", css=CSS)

    # Nota do usuário para este filme
    user_rating = session['ratings'].get(str(movie_id), 'Não avaliado')

    # Encontrar filmes similares com base nos gêneros
    similar_movies = []
    rated_movies_ids = {int(mid) for mid in session.get('ratings', {})}
    other_movies = {mid: m for mid, m in MOVIES.items() if mid != movie_id and mid not in rated_movies_ids}
    
    for mid, m in other_movies.items():
        score = 0
        for genre in movie["genres"]:
            if genre in m["genres"]:
                score += 1
        
        if score > 0:
            probability = round(sigmoid(score) * 100)
            similar_movies.append({
                "id": mid,
                "title": m["title"],
                "poster_url": m["poster_url"],
                "probability": probability,
                "genres": m["genres"]
            })
    
    similar_movies.sort(key=lambda x: x["probability"], reverse=True)
    
    return render_template_string(
        BASE_HTML + DETAILS_HTML,
        title=movie["title"],
        css=CSS,
        movie=movie,
        rating=user_rating,
        similar_movies=similar_movies[:5]
    )

@app.route('/watchlist')
def watchlist():
    if 'user_name' not in session:
        return redirect(url_for('home'))
        
    watchlist_ids = session.get('watchlist', [])
    watchlist_movies = [{"id": mid, **MOVIES[mid]} for mid in watchlist_ids if mid in MOVIES]
    
    return render_template_string(
        BASE_HTML + WATCHLIST_HTML,
        title="Minha Lista",
        css=CSS,
        watchlist=watchlist_movies
    )

@app.route('/my_scores')
def my_scores():
    if 'user_name' not in session:
        return redirect(url_for('home'))
        
    user_ratings = session.get('ratings', {})
    user_profile = calculate_user_profile(user_ratings)
    
    return render_template_string(
        BASE_HTML + MY_SCORES_HTML,
        title="Minhas Notas",
        css=CSS,
        scores=user_profile
    )

@app.route('/search')
def search():
    if 'user_name' not in session:
        return redirect(url_for('home'))
        
    query = request.args.get('query', '').lower()
    search_results = []
    
    if query:
        for mid, movie in MOVIES.items():
            if query in movie['title'].lower():
                search_results.append({"id": mid, **movie})

    return render_template_string(
        BASE_HTML + SEARCH_HTML,
        title="Busca",
        css=CSS,
        query=query,
        movies=search_results
    )

@app.route('/rate/<int:movie_id>/<int:rating>', methods=['POST'])
def rate_movie(movie_id, rating):
    if 'user_name' not in session or movie_id not in MOVIES or not (1 <= rating <= 5):
        return "Erro: Parâmetros inválidos", 400
    
    session.setdefault('ratings', {})
    session['ratings'][str(movie_id)] = rating
    
    # Recalcula o perfil do usuário e salva na sessão
    user_profile = calculate_user_profile(session['ratings'])
    session['user_profile'] = user_profile
    
    return "Avaliação registrada com sucesso!", 200

if __name__ == '__main__':
    app.run(debug=True)
