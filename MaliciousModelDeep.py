import pandas as pd
import numpy as np
import eli5
from eli5.sklearn import PermutationImportance
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
from tensorflow.keras.layers.experimental import RandomFourierFeatures
from tensorflow.keras.optimizers import SGD
import time
opt = SGD(lr=0.03)

malicious_combined = pd.read_csv("general_closenetwork_large_v1.csv", header=None)

dataset_combined = malicious_combined.values
X_Combined = dataset_combined[:, 0:18].astype(float)
Y_Combined = dataset_combined[:, 18]

# https://keras.io/guides/sequential_model/
def create_baseline():
	# create model
	
	malicious_model = tf.keras.Sequential([
    layers.Input(shape=(18,)),
	layers.Dense(50, activation='sigmoid'),
	layers.Dense(40, activation='sigmoid'),
	layers.Dense(25, activation='sigmoid'),
	layers.Dense(10, activation='sigmoid'),
	layers.Dense(1, activation='sigmoid')
    ])
	
	malicious_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'mean_absolute_percentage_error'])
	return malicious_model

# https://keras.io/examples/keras_recipes/quasi_svm/
def create_svm():
	# create model
	malicious_model = tf.keras.Sequential([
	RandomFourierFeatures(output_dim=4096, scale=10.0, kernel_initializer="gaussian"),
    layers.Dense(22),
    layers.Dense(1)
    ])
	malicious_model.compile(loss=tf.keras.losses.hinge, optimizer='adam', metrics=['accuracy'])
	return malicious_model

'''
start_time = time.time()
malicious_model = tf.keras.Sequential([
layers.Input(shape=(4,)),
layers.Dense(50, activation='sigmoid'),
layers.Dense(40, activation='sigmoid'),
layers.Dense(25, activation='sigmoid'),
layers.Dense(10, activation='sigmoid'),
layers.Dense(1, activation='sigmoid')
])
malicious_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'mean_absolute_percentage_error'])
history = malicious_model.fit(X_Combined, Y_Combined, validation_split=0.2, epochs=80, batch_size=20, verbose=2)
print("--- %s seconds ---" % (time.time() - start_time))

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

'''

# not enough data to do too many epochs
# svm_estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_svm, epochs=20, batch_size=5, verbose=0)
estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_baseline, epochs=80, batch_size=20, verbose=2)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
# svm_results = cross_val_score(svm_estimator, X, Y, cv=kfold)
results = cross_val_score(estimator, X_Combined, Y_Combined, cv=kfold)
# print("SVM Baseline: %.2f%% (%.2f%%)" % (svm_results.mean()*100, svm_results.std()*100))
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
