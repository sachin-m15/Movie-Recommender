import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=49b80bcb"
    response = requests.get(url)
    data = response.json()
    poster_url = data.get("Poster")

    # Check for "N/A" or missing poster
    if poster_url == "N/A" or poster_url is None:
        # Return a default placeholder image URL
        poster_url = "https://via.placeholder.com/500x750?text=No+Poster"

    return poster_url


def recommend(movie_name):
    movie_index = movies[movies["title"] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))

    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open("movie_dic.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommendation System")

options = st.selectbox("Select a movie", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(options)
    st.write("Recommendations based on your selection:", options)

    # Determine number of recommendations
    num_recs = len(names)

    # Dynamically create columns based on number of recommendations (max 5 shown)
    cols = st.columns(min(5, num_recs))
    for idx, col in enumerate(cols):
        if idx < num_recs:
            with col:
                st.text(names[idx])
                st.image(posters[idx])
