import streamlit as st
import pickle
import requests

# =========================
# CONFIG
# =========================
API_KEY = "66a55253e2e7653e8e38c661890fed6b"   
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER = "https://via.placeholder.com/300x450?text=No+Image"
import gdown
import os

def download_files():
    if not os.path.exists("movies.pkl"):
        gdown.download(
            "https://drive.google.com/uc?id=1TYC_U_s7qoIB8_0BGXLXRPhEBoiFJv_2",
            "movies.pkl",
            quiet=False
        )

    if not os.path.exists("similarity.pkl"):
        gdown.download(
            "https://drive.google.com/uc?id=1cXYQjKx4WqnkLBTVs0uULpPKs44hARKR",
            "similarity.pkl",
            quiet=False
        )

download_files()

# =========================
# LOAD DATA
# =========================
@st.cache_resource
def load_data():
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()
@st.cache_data(show_spinner=False)
def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        
        response = requests.get(url)
        data = response.json()

        print(data)   # 🔥 DEBUG (IMPORTANT)

        if data.get('results') and len(data['results']) > 0:
            poster_path = data['results'][0].get('poster_path')
            
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        return PLACEHOLDER

    except Exception as e:
        print("ERROR:", e)
        return PLACEHOLDER
@st.cache_data
def fetch_movie_details(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        data = requests.get(url).json()

        if not data['results']:
            return None

        movie_id = data['results'][0]['id']

        # movie details
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        details = requests.get(details_url).json()

        # credits (cast + crew)
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
        credits = requests.get(credits_url).json()

        cast = [c['name'] for c in credits['cast'][:3]]
        director = next((c['name'] for c in credits['crew'] if c['job'] == 'Director'), "N/A")

        return {
            "overview": details.get("overview", "No description"),
            "rating": details.get("vote_average", "N/A"),
            "cast": cast,
            "director": director
        }

    except:
        return None

# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]
    
    results = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        poster = fetch_poster(title)
        results.append((title, poster))
    
    return results

# =========================
# UI
# =========================
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>🎬 Movie Recommender</h1>",
    unsafe_allow_html=True
)

# 🔍 Search (with suggestions automatically)
selected_movie = st.selectbox(
    "Search for a movie",
    movies['title'].values
)

# =========================
# SHOW RESULTS
# =========================
if selected_movie:
    st.markdown("### Recommendations")

    with st.spinner("🎬 Finding movies..."):
        recommendations = recommend(selected_movie)

    # grid layout
    cols = st.columns(5)

for i, (title, poster) in enumerate(recommendations):
    with cols[i % 5]:
        st.image(poster)
        st.caption(title)

        with st.expander("View Details"):
            details = fetch_movie_details(title)

            if details:
                st.write(f"⭐ Rating: {details['rating']}")
                st.write(f"🎬 Director: {details['director']}")
                st.write(f"🎭 Cast: {', '.join(details['cast'])}")
                st.write(f"📝 {details['overview']}")
            else:
                st.write("No details available")
        
