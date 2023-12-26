import streamlit as st
import pickle as pkl
import pandas as pd
import requests

st.title('Movie Recommender System')


movies_dict = pkl.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity = pkl.load(open('similarity.pkl','rb'))

def fetchPosterUrl(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNGFiZGU5MGVkYzAzNmQ3NzE4MDc3NzRlY2JkZTdmNCIsInN1YiI6IjY1NzA2ZTMwZTFmYWVkMDBlMTdiZWJkYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.sjjNC2dlR6caWk9P0h--ezsOB32f9itD0KvIocFZ6o4"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    
    recommended_movies=[]
    recommended_movies_poster_link=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch movie poster
        recommended_movies_poster_link.append(fetchPosterUrl(movie_id))
    return recommended_movies,recommended_movies_poster_link




movies_list=movies['title']
selected_movie_name = st.selectbox(
    'Enter the movie name that you liked',
    (movies_list))

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.write(names[0])
        
    with col2:
        st.image(posters[1])
        st.write(names[1])

    with col3:
        st.image(posters[3])
        st.write(names[2])

    with col4:
        st.image(posters[3])
        st.write(names[3])

    with col5:
        st.image(posters[4])
        st.write(names[4])