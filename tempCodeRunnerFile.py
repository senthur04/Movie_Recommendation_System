return top_rated_movies.index.tolist()

recommended_movies = recommend_movies(10)
print(f"Recommended movies for user 10 : {recommended_movies}")