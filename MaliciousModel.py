import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
np.set_printoptions(precision=3, suppress=True)
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

malicious_train = pd.read_csv("malicious_train.csv", header=None)
malicious_test = pd.read_csv("malicious_test.csv")

malicious_train.head()
malicious_test.head()
print(malicious_train.values)
dataset = malicious_train.values
X = dataset[:, 0:4].astype(float)
Y = dataset[:, 4]

def create_baseline():
	# create model
	malicious_model = tf.keras.Sequential([
    layers.Dense(30),
    layers.Dense(1)
    ])
	malicious_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return malicious_model

estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_baseline, epochs=20, batch_size=5, verbose=0)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
