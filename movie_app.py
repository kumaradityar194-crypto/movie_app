import pickle
import streamlit as st
import requests
import os
import gdown

# ---------------- Download similarity.pkl from Google Drive ----------------
if not os.path.exists("similarity.pkl"):
    file_id = "1TUVeuwuSmz8G9V10TRP-iVLmcuXxjEqo"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "similarity.pkl", quiet=False)

# ---------------- Load Data ----------------
movies = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "1ed66bf10472a2200282e467c6d51499" 

# ---------------- Fetch Poster ----------------
def fetch_poster(title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
        return None
    except:
        return None


# ---------------- Recommend Movies ----------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    names, posters = [], []

    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        names.append(title)
        posters.append(fetch_poster(title))

    return names, posters


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.subheader(names[i])
            if posters[i]:
                st.image(posters[i], use_container_width=True)
            else:
                st.write("❌ Poster not available")

    st.markdown("---")
    st.markdown("### **Say Thanks to Kumar Aditya 🙌**")
