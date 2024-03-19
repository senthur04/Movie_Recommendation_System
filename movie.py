import pandas as pd
from sklearn.cluster import KMeans
#Input movies csv files
data = pd.read_csv('ratings.csv')
movies_data = pd.read_csv('movies.csv')

# Define the actual column name in your data 
title_column_name = 'title'

# Define the number of clusters (k)
k = 3

# Create KMeans object
kmeans = KMeans(n_clusters=k, random_state=0)

# Fit the model to the data || Clustering the data based on 2 features - movieId and rating
kmeans.fit(data[['movieId', 'rating']])

# Add a new column 'cluster' to the data containing the assigned cluster for each user-movie rating
data['cluster'] = kmeans.labels_

# Function to recommend movies for a user top rating movies
def recommend_movies(user_id):
  # Find the cluster label for the given user
  user_cluster = data[data['userId'] == user_id]['cluster'].iloc[0]
  # Get the list of movieIds that the user has rated
  user_rated_movies = data[data['userId'] == user_id]['movieId'].tolist()
  # Filter movies belonging to the same cluster as the user
  cluster_movies = data[data['cluster'] == user_cluster]
  # Filter out movies that the user has not rated
  unrated_movies = cluster_movies[~cluster_movies['movieId'].isin(user_rated_movies)]
  # Calculate the mean rating for each movie and sort in descending order, then take top 10
  top_rated_movies = unrated_movies.groupby('movieId')['rating'].mean().sort_values(ascending=False).head(10)
  # Return the list of movieIds of the recommended movies
  return top_rated_movies.index.tolist()

# Example usage: assuming user_id is 10
user_id = 10
recommended_movies = recommend_movies(user_id)

# Merge movie data with recommendations to get movie titles
recommended_movies_df = pd.DataFrame({'movieId': recommended_movies})
merged_data = recommended_movies_df.merge(movies_data, on='movieId')
# Extract the recommended movie titles as a list
recommended_movie_titles = merged_data[title_column_name].tolist()

# Print recommended movie titles
print(f"Recommended movie titles for user {user_id}: {recommended_movie_titles}")

def similar_movies(movie_title, k=10):
    # Check if the movie title exists in the dataset
    if movie_title in movies_data[title_column_name].values:
        # Find the movie ID based on title
        movie_id = movies_data[movies_data[title_column_name] == movie_title]['movieId'].iloc[0]
        # Filter movies based on similar genres
        similar_genres = movies_data[movies_data['movieId'] == movie_id]['genres'].iloc[0]
        #From similar genre , find similar movies
        similar_movies = movies_data[movies_data['genres'].str.contains(similar_genres, case=False)]
        # Exclude the input movie and sort by rating
        similar_movies = similar_movies[similar_movies['title'] != movie_title].head(k)

        return similar_movies[title_column_name].tolist()
    else:
        print("Movie not found in the dataset. Please enter a valid movie title.")

# Example usage: enter a movie title
movie_title = input("Enter movie title: ")

# Check if the movie title exists in the dataset
if movie_title in movies_data[title_column_name].values:
    similar_movies_list = similar_movies(movie_title)
    print(f"Similar movies to '{movie_title}':")
    for movie in similar_movies_list:
        print(movie)
else:
    print("Movie not found in the dataset.")
