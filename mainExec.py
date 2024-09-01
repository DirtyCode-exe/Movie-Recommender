import pandas as pd
import os
import joblib

from loadData import prepare_movie_data, data_chunks
from generateRecommend import generate_combined_recommendations, movie_id_to_tags
from model import train_and_save_model, load_model, model_path

# Check if the model already exists
if os.path.exists(model_path):
    algo = load_model(model_path)
else:
    # Train the model and save it
    algo = train_and_save_model(data_chunks, model_path)

movie_name_to_id, movie_id_to_name, movie_id_to_genre, movie_id_to_year = prepare_movie_data('movies.csv')
url='https://drive.google.com/file/d/1CfkNYSDh0kNq43VHmOHsNaxQ5gmLYXK6/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
movies = pd.read_csv(url)
movies.dropna(inplace=True)

# Collect user input for favorite movie names
user_favorites_names = input("Enter your favorite movies separated by commas: ").split(',')
user_favorites_names = [name.strip().lower() for name in user_favorites_names]

# Convert movie names to IDs
user_favorites_ids = [movie_name_to_id.get(name, None) for name in user_favorites_names]
user_favorites_ids = [id for id in user_favorites_ids if id is not None]

user_id = 'new_user'

# Generate recommendations
generate_combined_recommendations(algo, user_id, movie_id_to_name, movie_id_to_genre, movie_id_to_year, movie_id_to_tags, user_favorites_ids)
