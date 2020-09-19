# Neural network on personality traits
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import matplotlib.pyplot as plt

def neural_network(path):
	# load the dataset
	dataset = loadtxt(path, skiprows=1, delimiter=',')
	# split into input (X) and output (y) variables
	X = dataset[:, 0:16]
	y = dataset[:, 16]

	# define the keras model
	model = Sequential()
	model.add(Dense(10, input_dim=16, activation='relu'))
	model.add(Dense(6, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))

	model.summary()

	# compile the keras model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


	# fit the keras model on the dataset
	history = model.fit(X, y, epochs=40, batch_size=32)
	# list all data in history
	print(history.history.keys())
	# summarize history for accuracy
	plt.plot(history.history['accuracy'])
	#plt.plot(history.history['val_accuracy'])
	plt.title('model accuracy')
	plt.ylabel('accuracy')
	plt.xlabel('epoch')
	plt.legend(['train', 'test'], loc='upper left')
	plt.show()
	# summarize history for loss
	plt.plot(history.history['loss'])
	#plt.plot(history.history['val_loss'])
	plt.title('model loss')
	plt.ylabel('loss')
	plt.xlabel('epoch')
	plt.legend(['train', 'test'], loc='upper left')
	plt.show()


	# save model and architecture to single file
	model.save("model.h5")
	print("Saved model to disk")

def test_neural_network(path_test):
	# load model
	model = load_model('model.h5')
	# summarize model.
	model.summary()

	# load the dataset
	dataset = loadtxt(path_test, skiprows=1, delimiter=',')
	# split into input (X) and output (y) variables
	X = dataset[:, 0:16]
	y = dataset[:, 16]

	# evaluate the keras model
	_, accuracy = model.evaluate(X, y)
	print('Accuracy: %.2f' % (accuracy*100))

	# make class predictions with the model
	predictions = model.predict_classes(X)
	# summarize the first 50 cases
	for i in range(50):
		print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))

if __name__ == "__main__":
	neural_network('final_personalitytraits_train.csv')
	test_neural_network('final_personalitytraits_test.csv')