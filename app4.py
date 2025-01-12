import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    # Properly format the URL with the movie_id
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7af5a6c1467e31be19a503dec4910e25&language=en-us"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    # Find the index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    # Get similarity scores for the selected movie
    distances = similarity[movie_index]
    # Sort movies by similarity score and get the top 5 similar movies
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    "Enter the name of a movie", movies['title'].values
)

if st.button('Recommend'):
    # Get recommendations
    names, posters = recommend(selected_movie_name)

    # Create columns to display recommended movies and their posters
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
