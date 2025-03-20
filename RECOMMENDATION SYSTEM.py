import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_movie_recommendation_system():
    # Sample movie dataset
    movies = pd.DataFrame({
        'title': ['Inception', 'Interstellar', 'The Matrix', 'The Dark Knight', 'Avatar'],
        'description': [
            'A thief who enters the dreams of others to steal secrets. A mind-bending sci-fi thriller.',
            'A team of explorers travel through a wormhole in space in an attempt to ensure humanity’s survival.',
            'A hacker discovers the shocking truth about his reality and fights against a powerful AI.',
            'A vigilante superhero fights crime in Gotham City and faces his greatest enemy, the Joker.',
            'A paraplegic marine embarks on a journey to another world and gets involved in a war between civilizations.'
        ]
    })
    
    # Convert text to numerical features using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(movies['description'])
    
    # Compute cosine similarity between movies
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    def recommend_movies(movie_title, top_n=3):
        if movie_title not in movies['title'].values:
            return "Movie not found. Try another title."
        
        movie_idx = movies[movies['title'] == movie_title].index[0]
        similarity_scores = list(enumerate(similarity_matrix[movie_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        recommended_movie_indices = [i[0] for i in similarity_scores[1:top_n+1]]
        
        return movies.iloc[recommended_movie_indices]['title'].tolist()
    
    return recommend_movies

# Example Usage:
# recommender = create_movie_recommendation_system()
# print(recommender('Inception'))