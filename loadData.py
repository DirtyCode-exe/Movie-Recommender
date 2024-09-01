###########Load and Prepare Data
import gdown
import pandas as pd
from surprise import Dataset, Reader

def load_data(file_path, chunk_size=100000):
    reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 5))
    data_chunks = []

    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        data_chunks.append(chunk[['userId', 'movieId', 'rating']])

    return data_chunks

def prepare_movie_data(movies_file):
    movies_df = pd.read_csv(movies_file)
    movie_name_to_id = pd.Series(movies_df.movieId.values, index=movies_df.name.str.lower()).to_dict()
    movie_id_to_name = pd.Series(movies_df.name.values, index=movies_df.movieId).to_dict()
    movie_id_to_genre = movies_df.set_index('movieId').genres.str.split('|').to_dict()
    movie_id_to_year = pd.Series(movies_df.year.values, index=movies_df.movieId).to_dict()

    return movie_name_to_id, movie_id_to_name, movie_id_to_genre, movie_id_to_year

url='https://drive.google.com/file/d/1lZ66f02CpjHgeyrmnZDBMNbw-ZJVLA9E/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
#test=pd.read_csv(url)
import gdown
gdown.download('https://drive.google.com/uc?export=download&id=1lZ66f02CpjHgeyrmnZDBMNbw-ZJVLA9E', output='filename', quiet=False)
data_chunks = load_data("ratings.csv")
