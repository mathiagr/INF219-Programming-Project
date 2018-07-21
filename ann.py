# Artificial Neural Network

# Installing Theano
# pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git

# Installing Tensorflow
# Install Tensorflow from the website: https://www.tensorflow.org/versions/r0.12/get_started/os_setup.html

# Installing Keras
# pip install --upgrade keras
# Part 1 - Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('data_tf.csv')
X = dataset.iloc[:, 1:].values
y = dataset.iloc[:, 0].values



# =============================================================================
# 
# # Encoding categorical data
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# labelencoder_X_1 = LabelEncoder()
# X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
# labelencoder_X_2 = LabelEncoder()
# X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
# onehotencoder = OneHotEncoder(categorical_features = [1])
# X = onehotencoder.fit_transform(X).toarray()
# X = X[:, 1:] #Removing one DV to avoid the Dummy Variable Trap.
# 
# =============================================================================
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Part 2 - Now let's make the ANN!

# Importing the Keras libraries and packages
import keras #FOR AT DISSE SKAL VIRKE MAA SPYDER AAPNER FRA py35 shell
# source activate py35
# spyder
from keras.models import Sequential
from keras.layers import Dense

# Initialising the ANN
# Defining it as a sequence of layers 
classifier = Sequential() #an object of the sequential class

# Adding the input layer and the first hidden layer
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu', input_dim = 11))
# We use the rectifier function (relu) for the hidden layers
# and the sigmoid function for the output layer
#Output dim is (11+1)/2 the average of nodes in output and input layers. This is the number of nodes in the hidden layer
#init, we randomly initialize the weights with a function (uniform)

# Adding the second hidden layer
classifier.add(Dense(output_dim = 6, init = 'uniform', activation = 'relu'))

# Adding the output layer
classifier.add(Dense(output_dim = 1, init = 'uniform', activation = 'sigmoid')) 
#we want probabilities for outcome so we use sigmoid
#if the DV has more than 2 categories we must enter output dim to number of DVs and use 'softmax' (sigmoid for several DVs)

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
#optimizer algorithm to find the optimal weights, we use 'adam' which is a SGD algo
#SGD is based on a loss function. We use binary_crossentropy (which is a logarithmic loss function)
#If our DV has har than 2 outcomes (0/1) we use the categorical_crossentropy as a loss function
#metrics is the creterion we use to evaluate the model


# Fitting the ANN to the Training set
classifier.fit(X_train, y_train, batch_size = 10, nb_epoch = 100)
#Batch size is number of observations after which we change weights
#nb_epoch is number of epochs, which is when the w


# Part 3 - Making the predictions and evaluating the model

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)