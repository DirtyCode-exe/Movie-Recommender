######Generate Recommendations

import random

import pandas as pd
from surprise import Dataset

def get_similar_movies(movie_id, movie_id_to_tags, top_n=10):
    if movie_id not in movie_id_to_tags:
        return []

    target_tags = set(movie_id_to_tags[movie_id])
    similar_movies = []
    for other_movie_id, tags in movie_id_to_tags.items():
        if other_movie_id != movie_id:
            common_tags = target_tags.intersection(tags)
            if common_tags:
                similar_movies.append((other_movie_id, len(common_tags)))

    similar_movies.sort(key=lambda x: x[1], reverse=True)
    return [movie_id for movie_id, _ in similar_movies[:top_n]]

def generate_combined_recommendations(algo, user_id, id_to_name, id_to_genre, id_to_year, id_to_tags, user_favorites, top_n=10):
    user_genres = set()
    user_years = []
    for movie_id in user_favorites:
        if movie_id in id_to_genre:
            user_genres.update(id_to_genre[movie_id])
        if movie_id in id_to_year:
            user_years.append(id_to_year[movie_id])

    if user_years:
        min_year = int(min(user_years) - 5)
        max_year = int(max(user_years) + 35)
    else:
        min_year = 0
        max_year = 0

    all_movie_ids = set(id_to_name.keys())
    filtered_movie_ids = []
    for movie_id in all_movie_ids:
        if movie_id in id_to_genre and movie_id in id_to_year:
            movie_genres = set(id_to_genre[movie_id])
            movie_year = id_to_year[movie_id]
            if (user_genres.issubset(movie_genres) and
                (min_year <= movie_year <= max_year)):
                filtered_movie_ids.append(movie_id)

    # Randomly shuffle filtered movie IDs
    random.shuffle(filtered_movie_ids)

    # Get predictions for filtered movies
    predictions = [algo.predict(user_id, movie_id) for movie_id in filtered_movie_ids]
    sorted_predictions = sorted(predictions, key=lambda x: x.est, reverse=True)

    top_recommendations = {pred.iid: pred.est for pred in sorted_predictions[:top_n]}
    top_recommendations = {k: v for k, v in top_recommendations.items() if k not in user_favorites}

    # Incorporate tag-based recommendations
    c=220
    for movie_id in user_favorites:
        similar_movies = get_similar_movies(movie_id, id_to_tags, top_n)
        for sim_movie_id in similar_movies:
            if sim_movie_id not in top_recommendations:
                if sim_movie_id in id_to_year:
                    sim_movie_year = id_to_year[sim_movie_id]
                    if (min_year is not None and max_year is not None and
                        min_year <= sim_movie_year <= max_year):
                        top_recommendations[sim_movie_id] = c
                        c= c-1
    top_recommendations = {k: v for k, v in top_recommendations.items() if k not in user_favorites}

    # Sort by estimated rating or default value
    sorted_top_recommendations = sorted(top_recommendations.items(), key=lambda x: x[1], reverse=True)
    random.shuffle(sorted_top_recommendations)
    print("Combined Recommendations:")
    moviesList = []
    for movie_id, rating in sorted_top_recommendations[:top_n]:
        movie_name = id_to_name.get(movie_id, "Unknown Movie")
        print(f"Recommended Movie: {movie_name} with rating: {rating:.2f}")
        moviesList.append(movie_name)
    print(len(sorted_top_recommendations))
    return moviesList
url='https://drive.google.com/file/d/1bkr8Cr3DSOUEncU-A1wme7pEYQCw9SQa/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
tags_df = pd.read_csv(url)
print(tags_df)
tags_df.dropna(inplace=True)


# Create a dictionary to map movie IDs to tags (as lists)
movie_id_to_tags = tags_df.groupby('movieId')['tag'].apply(lambda x: list(x)).to_dict()