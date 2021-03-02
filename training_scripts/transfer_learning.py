from keras.applications import VGG16
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt

#Initialises the base premade model
conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(150, 150, 3))

#don't edit the weights of the prebuilt model
conv_base.trainable = False

#directories with the buy/sell folders 
train_dir = './data/train'
validation_dir = './data/validate'
test_dir = validation_dir

#determine num. of epochs & batch size
batch_size = 20
epochs = 100

#rescale images to be arrays of numbers between 0 & 1
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    # All images will be resized to 150x150
    target_size=(150, 150),
    batch_size=20,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=20,
    class_mode='binary')

#build the rest of the model around the prebuilt base
model = Sequential()
model.add(conv_base)
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

#compile model with a low learning rate
model.compile(optimizer=RMSprop(lr=2e-5),
              loss='binary_crossentropy',
              metrics=['acc'])

#print model details
model.summary()

#train model
history = model.fit_generator(
      train_generator,
      steps_per_epoch=1000//batch_size,
      epochs=epochs,
      validation_data=validation_generator,
      validation_steps=200//batch_size,
      shuffle=True)

#save the model & weights
model.save('./models/model.h5')
model.save_weights('./models/weights')

#plot the metrics of the model training
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
