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
# tf.disable_v2_behavior() 
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing


'''
inputs = tf.keras.Input(shape=(784,), name = "digits")
x = layers.Dense(64, activation="relu", name="dense_1")(inputs)
x = layers.Dense(64, activation="relu", name="dense_2")(x)
outputs = layers.Dense(10, activation="softmax", name="predictions")(x)
print(inputs)
print(outputs)
model = tf.keras.Model(inputs=inputs, outputs=outputs)

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print("X TRAIN: ", x_train)
print("Y TRAIN: ", y_train)
print("X TEST: ", x_test)
print("Y TEST: ", y_test)

# Preprocess the data (these are NumPy arrays)
x_train = x_train.reshape(60000, 784).astype("float32") / 255
x_test = x_test.reshape(10000, 784).astype("float32") / 255

y_train = y_train.astype("float32")
y_test = y_test.astype("float32")

# Reserve 10,000 samples for validation
x_val = x_train[-10000:]
y_val = y_train[-10000:]
x_train = x_train[:-10000]
y_train = y_train[:-10000]

model.compile(
    optimizer=tf.keras.optimizers.RMSprop(),  # Optimizer
    # Loss function to minimize
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    # List of metrics to monitor
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)
history = model.fit(
    x_train,
    y_train,
    batch_size=64,
    epochs=2,
    # We pass some validation for
    # monitoring validation loss and metrics
    # at the end of each epoch
    validation_data=(x_val, y_val),
)
print(history.history)
# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(x_test, y_test, batch_size=128)
print("test loss, test acc:", results)

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print("Generate predictions for 3 samples")
predictions = model.predict(x_test[:3])
print("predictions shape:", predictions.shape)
'''
def feature_normalize(dataset):
    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    return (dataset-mu)/sigma

def str_to_int(df):
    str_columns = df.select_dtypes(['object']).columns
    print(str_columns)
    for col in str_columns:
        df[col] = df[col].astype('category')

    cat_columns = df.select_dtypes(['category']).columns
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
    return df

def count_space_except_nan(x):
    if isinstance(x,str):
        return x.count(" ") + 1
    else :
        return 0

# https://stackoverflow.com/a/42523230
def one_hot(df, cols):
    """
    @param df pandas DataFrame
    @param cols a list of columns to encode 
    @return a DataFrame with one-hot encoding
    """
    for each in cols:
        dummies = pd.get_dummies(df[each], prefix=each, drop_first=False)
        del df[each]
        df = pd.concat([df, dummies], axis=1)
    return df

def pre_processing(df):
    df["bitcoin_spent"].fillna(df["bitcoin_spent"].mean(), inplace=True)
    df["bitcoin_received"].fillna(df["bitcoin_received"].mean(), inplace=True)
    df["total_balance"].fillna(df["total_balance"].mean(), inplace=True)
    df["total_transactions"].fillna(df["total_transactions"].mean(), inplace=True)
    df = str_to_int(df)

    df["bitcoin_spent"] = feature_normalize(df["bitcoin_spent"])
    df["bitcoin_received"] = feature_normalize(df["bitcoin_received"])
    df["total_balance"] = feature_normalize(df["total_balance"])
    df["total_transactions"] = feature_normalize(df["total_transactions"])
    stats.describe(df).variance
    return df

malicious_train = pd.read_csv("malicious_train.csv", header=None)
malicious_test = pd.read_csv("malicious_test.csv")

malicious_train.head()
malicious_test.head()
print(malicious_train.values)
dataset = malicious_train.values
X = dataset[:, 0:4].astype(float)
Y = dataset[:, 4]

'''
malicious_features = malicious_train.copy()
malicious_labels = malicious_features.pop('malicious')
malicious_test_features = malicious_test.copy()
malicious_test_labels = malicious_test_features.pop('malicious')

malicious_features = np.array(malicious_features)
malicious_test_features = np.array(malicious_test_features)
normalize = preprocessing.Normalization()
normalize.adapt(malicious_features)
normalize.adapt(malicious_test_features)

'''

def create_baseline():
	# create model
	malicious_model = tf.keras.Sequential([
    layers.Dense(30),
    layers.Dense(1)
    ])
	malicious_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return malicious_model

'''
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_baseline, epochs=20, batch_size=5, verbose=0)))
pipeline = Pipeline(estimators)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(pipeline, X, Y, cv=kfold)
print("Smaller: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

'''
# malicious_model.fit(malicious_features, malicious_labels, epochs = 10)
estimator = tf.keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_baseline, epochs=20, batch_size=5, verbose=0)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
