########Train the Model
import pandas as pd
from surprise import SVD, Reader, Dataset
import joblib
import os
from loadData import data_chunks

model_path='recommendation_model.pkl'


def train_and_save_model(data_chunks, model_path):
    algo = SVD()  # Use SVD algorithm for collaborative filtering

    # Combine all chunks into a single DataFrame
    combined_df = pd.concat(data_chunks, ignore_index=True)

    # Create a Dataset and a Trainset from the combined DataFrame
    reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 5))
    data = Dataset.load_from_df(combined_df, reader)
    trainset = data.build_full_trainset()

    # Fit the model on the combined trainset
    algo.fit(trainset)

    # Save the trained model
    joblib.dump(algo, model_path)
    return algo

def load_model(model_path):
    # Load the saved model

    return joblib.load(model_path)
