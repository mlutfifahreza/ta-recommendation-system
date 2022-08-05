print('# 1. Import Libraries')
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# Now let’s look at what dataset we will be working with.

print('# 2. Load the Dataset')
# We will be working with a very simple dataset today i.e the iris dataset. We will load the dataset using load_iris() function, which is part of the scikit-learn library. The dataset consists of three main classes. We will divide them into target variables and features.
# Loading dataset
data = load_iris()
# Dividing the dataset into target variable and features
X=data.data
y=data.target

print('# 3. Split Dataset in Training and Testing')
# Now we will split the dataset into training and test sets. We will use the function train_test_split(). The function takes three parameters: the features, target, and size of the test set.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=20, random_state=4)
# Now in the next step, we have to start initializing the hyperparameters. We will input the learning rate, iterations, input size, number of hidden layers, and number of output layers.
learning_rate = 0.1
iterations = 5000
N = y_train.size
 # Input features
input_size = 4
# Hidden layers 
hidden_size = 2
# Output layer
output_size = 3  
results = pd.DataFrame(columns=['mse', 'accuracy'])

print('# 3. Initialize Weights')
np.random.seed(10) 
# Hidden layer
W1 = np.random.normal(scale=0.5, size=(input_size, hidden_size))   
# Output layer
W2 = np.random.normal(scale=0.5, size=(hidden_size , output_size)) 
# Now we will create helper functions such as mean squared error, accuracy and sigmoid.
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def mean_squared_error(y_pred, y_true):
    return ((y_pred - y_true)**2).sum() / (2*y_pred.size)
def accuracy(y_pred, y_true):
    acc = y_pred.argmax(axis=1) == y_true.argmax(axis=1)
    return acc.mean()
# Now we will start building our backpropagation model.

print('# 4. Building the Backpropogation Model in Python')
# We will create a for loop for a given number of iterations and will update the weights in each iteration. The model will go through three phases feedforward propagation, the error calculation phase, and the backpropagation phase.
for itr in range(iterations):    
    # Implementing feedforward propagation on hidden layer
    Z1 = np.dot(X_train, W1)
    A1 = sigmoid(Z1)
    # Implementing feed forward propagation on output layer
    Z2 = np.dot(A1, W2)
    A2 = sigmoid(Z2)
    # Calculating the error
    mse = mean_squared_error(A2, y_train)
    acc = accuracy(A2, y_train)
    results=results.append({'mse':mse, 'accuracy':acc},ignore_index=True )
    # Backpropagation phase
    E1 = A2 - y_train
    dW1 = E1 * A2 * (1 - A2)
 
    E2 = np.dot(dW1, W2.T)
    dW2 = E2 * A1 * (1 - A1)
    # Updating the weights
    W2_update = np.dot(A1.T, dW1) / N
    W1_update = np.dot(X_train.T, dW2) / N
 
    W2 = W2 - learning_rate * W2_update
    W1 = W1 - learning_rate * W1_update
print('# Now we will plot the mean squared error and accuracy using the pandas plot() function.')

results.mse.plot(title='Mean Squared Error')
# Download
results.accuracy.plot(title='Accuracy')
# Download 1
print('# Now we will calculate the accuracy of the model.')

Z1 = np.dot(X_test, W1)
A1 = sigmoid(Z1)
 
Z2 = np.dot(A1, W2)
A2 = sigmoid(Z2)
 
acc = accuracy(A2, y_test)
print('Accuracy: {}'.format(acc))
# Output:
# Accuracy: 0.8
print('# You can see the accuracy of the model have been significantly increased to 80%.')