import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import RandomFourierFeatures
import time

data = pd.read_csv("ftx_large_v3.csv", header=None)

# Reading in data, separating criminal binary into Y and features into X
dataset = data.values
X = dataset[:, 0:19].astype(float)
Y = dataset[:, 19]

# Deep Neural Network creation function
def create_deep_nn():	
	malicious_model = tf.keras.Sequential([
    layers.Input(shape=(19,)),
	layers.Dense(100, activation='sigmoid'),
	layers.Dense(50, activation='sigmoid'),
	layers.Dense(25, activation='sigmoid'),
	layers.Dense(12, activation='sigmoid'),
	layers.Dense(1, activation='sigmoid')
    ])
	malicious_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy', 'mean_absolute_percentage_error'])
	return malicious_model


# SVM creation function
'''
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

# For plotting performance graphs and measuring training time
'''
start_time = time.time()
malicious_model = tf.keras.Sequential([
layers.Input(shape=(19,)),
layers.Dense(100, activation='sigmoid'),
layers.Dense(50, activation='sigmoid'),
layers.Dense(25, activation='sigmoid'),
layers.Dense(12, activation='sigmoid'),
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

# SVM Cross Validation
'''
svm_estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_svm, epochs=20, batch_size=5, verbose=0)
svm_results = cross_val_score(svm_estimator, X, Y, cv=kfold)
print("SVM Baseline: %.2f%% (%.2f%%)" % (svm_results.mean()*100, svm_results.std()*100))
'''

# Deep Neural Network Cross Validation
estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_deep_nn, epochs=80, batch_size=20, verbose=2)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
