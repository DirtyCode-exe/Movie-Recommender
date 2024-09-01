import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import math
# import seaborn as sns
# import scipy.stats as stats
from sklearn.model_selection import train_test_split
from surprise import Dataset, Reader, KNNBasic , SVD , SVDpp
from surprise.model_selection import train_test_split
from surprise import accuracy
from surprise.model_selection import PredefinedKFold
from flask import Flask, request, render_template
# from flask_ngrok import run_with_ngrok
# import ngrok
