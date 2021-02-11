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
opt = SGD(lr=0.01)

malicious_combined = pd.read_csv("additional_small.csv", header=None)
malicious_train = pd.read_csv("malicious_train_bitcoinabuse.csv", header=None)
malicious_test = pd.read_csv("malicious_test_bitcoinabuse.csv", header=None)

malicious_train.head()
malicious_test.head()

dataset_combined = malicious_combined.values
X_Combined = dataset_combined[:, 0:24].astype(float)
Y_Combined = dataset_combined[:, 24]

dataset = malicious_train.values
X = dataset[:, 0:4].astype(float)
Y = dataset[:, 4]

dataset_test = malicious_test.values
X_Test = dataset_test[:, 0:4].astype(float)
Y_Test = dataset_test[:, 4]

# https://keras.io/guides/sequential_model/
def create_baseline():
	# create model
	malicious_model = tf.keras.Sequential([
	layers.Dense(25, activation='relu'),
	layers.Dense(13, activation='sigmoid'),
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
malicious_model = tf.keras.Sequential([
layers.Dense(5, activation='sigmoid'),
layers.Dense(3, activation='sigmoid'),
layers.Dense(1)
])
malicious_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'mean_absolute_percentage_error'])

# stochastic gradient descent best performing, batch size = 1


history = malicious_model.fit(X, Y, epochs=200, batch_size=10, verbose=2)
results = malicious_model.evaluate(X_Test, Y_Test, batch_size=10, verbose = 0)
print("test loss, test acc:", results)
'''

# plot metrics
# plt.plot(history.history['mean_absolute_percentage_error'])
# plt.plot(history.history['accuracy'])
# plt.show()
# plt.close()


# not enough data to do too many epochs
# svm_estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_svm, epochs=20, batch_size=5, verbose=0)
estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_baseline, epochs=80, batch_size=20, verbose=2)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
# svm_results = cross_val_score(svm_estimator, X, Y, cv=kfold)
results = cross_val_score(estimator, X_Combined, Y_Combined, cv=kfold)
# print("SVM Baseline: %.2f%% (%.2f%%)" % (svm_results.mean()*100, svm_results.std()*100))
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))


'''
perm = PermutationImportance(malicious_model, cross_val_score(estimator, X, Y, cv=kfold))
eli5.explain_weights(perm, feature_names = X.columns.tolist())
'''