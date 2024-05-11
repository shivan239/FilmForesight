import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=74766850ca41fdf550a9e13cc7027e48'.format(movie_id))

    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/original/" + poster_path
        else:
            return "No poster available"
    else:
        return "API request failed"


# Replace 'YOUR_API_KEY' with your actual TMDb API key.




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters




from googlesearch import search as google_search
from pytube import YouTube
import time
import webbrowser


def get_youtube_link_for_movie(movie_name):
    query = f"{movie_name} trailer"

    try:
        # Search for the movie trailer on Google
        search_results = google_search(query, num=5, stop=5, pause=2)

        # Check each search result for a YouTube link
        for result in search_results:
            if 'youtube.com' in result:
                return result
            time.sleep(1)  # Add a delay to avoid rate limiting

        print("No YouTube link found in search results.")
    except Exception as e:
        print(f"Error while searching for {movie_name} trailer: {e}")

    return None


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('movie recommender system')

selected_movie_name = st.selectbox(
    'WELCOME TO MOVIE HUB',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    if st.button('watch_1'):
        youtube_link = get_youtube_link_for_movie(names[0])
        if youtube_link:
            webbrowser.open(youtube_link, new=2)


    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.button('watch_2')

    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.button('watch_3')

    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.button('watch_4')

    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.button('watch_5')


