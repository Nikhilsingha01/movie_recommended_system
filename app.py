import streamlit as st
import pickle
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Load the data
@st.cache_data
def load_data():
    try:
        movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError as e:
        st.error(f"Error loading data files: {e}")
        st.stop()

movies, similarity = load_data()

def recommend(movie):
    """Get movie recommendations based on similarity"""
    try:
        # Find the movie index
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
        return recommended_movies
    except IndexError:
        st.error("Movie not found in the database.")
        return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Main UI
st.title('🎬 Movie Recommender System')
st.markdown("---")

# Sidebar for movie selection
st.sidebar.header("Select a Movie")
selected_movie = st.sidebar.selectbox(
    'Choose a movie you like:',
    movies['title'].values,
    index=0
)

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Your Selection")
    st.write(f"**{selected_movie}**")
    
    if st.button('🔍 Get Recommendations', type="primary", use_container_width=True):
        with st.spinner('Finding similar movies...'):
            recommendations = recommend(selected_movie)
            
            if recommendations:
                st.session_state.recommendations = recommendations
                st.session_state.selected_movie = selected_movie

with col2:
    st.subheader("Recommended Movies")
    
    if 'recommendations' in st.session_state and st.session_state.recommendations:
        st.write(f"Movies similar to **{st.session_state.selected_movie}**:")
        st.markdown("---")
        
        for idx, movie in enumerate(st.session_state.recommendations, 1):
            st.markdown(f"**{idx}.** {movie}")
    else:
        st.info("👈 Select a movie and click 'Get Recommendations' to see similar movies!")

# Footer
st.markdown("---")
st.markdown("### About")
st.markdown("This movie recommender system uses content-based filtering to suggest movies similar to your selection based on genres, keywords, cast, crew, and overview.")

