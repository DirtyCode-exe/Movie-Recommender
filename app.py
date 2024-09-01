from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import os
import logging

from loadData import prepare_movie_data
from generateRecommend import generate_combined_recommendations, movie_id_to_tags
from model import load_model, model_path, train_and_save_model, data_chunks

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
url='https://drive.google.com/file/d/1CfkNYSDh0kNq43VHmOHsNaxQ5gmLYXK6/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
movies_df =  pd.read_csv(url)

# Load the model on startup
if os.path.exists(model_path):
    logging.debug("Loading model from disk.")
    algo = load_model(model_path)
else:
    logging.debug("Training model.")
    algo = train_and_save_model(data_chunks, model_path)

# Prepare movie data
logging.debug("Preparing movie data.")
movie_name_to_id, movie_id_to_name, movie_id_to_genre, movie_id_to_year = prepare_movie_data('movies.csv')
movies_df.dropna(inplace=True)

@app.route('/')
def home():
  logging.debug("home accessed!")
  return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    print(f"Search keyword: {query}")  # Debugging statement
    if query:
        movies_df['title'] = movies_df['title'].astype(str)
        # logging.debug(f"Searching for: {movies_df[movies_df['title']]}")  # Log the results
        results = movies_df[movies_df['title'].str.lower().str.contains(query, regex=False, na=False)]
        logging.debug(f"results: {results}")  # Log the results
        results_list = results[['movieId', 'title']].to_dict(orient='records')
        logging.debug(f"results list: {results_list}")  # Log the results

        return jsonify(results_list)
    return jsonify([])

@app.route('/recommend', methods=['POST'])
def recommend():
    logging.debug("Received request for recommendations.")
    try:

        user_favorites_names = request.form.get('favorites','')
        user_favorites_names = [title.strip().lower() for title in user_favorites_names.split(',')]
        logging.debug(f"User favorites: {user_favorites_names}")

        # Convert movie names to IDs
        user_favorites_ids = [movie_name_to_id.get(title, None) for title in user_favorites_names]
        user_favorites_ids = [id for id in user_favorites_ids if id is not None]
        logging.debug(f"User favorite IDs: {user_favorites_ids}")

        user_id = 'new_user'

        # Generate recommendations
        recommendations = generate_combined_recommendations(
            algo, user_id, movie_id_to_name, movie_id_to_genre, movie_id_to_year, movie_id_to_tags, user_favorites_ids
        )

        logging.debug(f"Recommendations: {recommendations}")
        return jsonify(recommendations)
    except Exception as e:
        logging.error("Error occurred: ", exc_info=True)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))  # Use the PORT environment variable, default to 5050
    app.run(host='0.0.0.0', port=port, debug=True)
