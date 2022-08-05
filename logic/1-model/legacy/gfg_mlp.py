# importing modules
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Cast the records into float values
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

# normalize image pixel values by dividing
# by 255
gray_scale = 255
x_train /= gray_scale
x_test /= gray_scale

print('Feature matrix:', x_train.shape)
print('Target matrix:', x_test.shape)
print('Feature matrix:', y_train.shape)
print('Target matrix:', y_test.shape)

fig, ax = plt.subplots(10, 10)
k = 0
for i in range(10):
	for j in range(10):
		ax[i][j].imshow(x_train[k].reshape(28, 28),
						aspect='auto')
		k += 1
# plt.show()

model = Sequential([
	
	# reshape 28 row * 28 column data to 28*28 rows
	Flatten(input_shape=(28, 28)),
	
	# dense layer 1
	Dense(256, activation='sigmoid'),
	
	# dense layer 2
	Dense(128, activation='sigmoid'),
	
	# output layer
	Dense(10, activation='sigmoid'),
])

model.compile(optimizer='adam',
			loss='sparse_categorical_crossentropy',
			metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10,
		batch_size=2000,
		validation_split=0.2)

results = model.evaluate(x_test, y_test, verbose = 0)
print('test loss, test acc:', results)
