import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model, model_from_json

img_width, img_height = 150, 150
#load in the model
#model_path = './models/model'
#weights_path = './models/weights'
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

data_path = './data/validate'

#print model details
model.summary()

#get the prediction for a specific file
def predict(file):
  x = load_img(file, target_size=(150,150,3))
  x = img_to_array(x)
  print(x.shape)
  x = np.expand_dims(x, axis=0)
  array = model.predict(x)
  result = array[0]
  if result[0] < 0.05:
    print("Predicted answer: Buy")
    answer = 'buy'
    print(result)
  elif result[0] > 0.95:
    print("Predicted answer: Sell")
    answer = 'sell'
    print(result)
  else:
    print("Predicted answer: Not confident")
    answer = 'n/a'
    print(result)

  return answer

tb = 0
ts = 0
fb = 0
fs = 0
na = 0

#run predictions for all images in the buy & sell folders of the given data path
for i, ret in enumerate(os.walk(data_path + '/buy')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
    print("Label: buy")
    result = predict(ret[0] + '/' + filename)
    if result == "buy":
      tb += 1
    elif result == 'n/a':
      print('no action')
      na += 1
    else:
      fb += 1

for i, ret in enumerate(os.walk(data_path + '/sell')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
    print("Label: sell")
    result = predict(ret[0] + '/' + filename)
    if result == "sell":
      ts += 1
    elif result == 'n/a':
      print('no action')
      na += 1
    else:
      fs += 1

#print the results 
print("True buy: ", tb)
print("True sell: ", ts)
print("False buy: ", fb)  # important
print("False sell: ", fs)
print("No action", na)

precision = (tb+ts) / (tb + ts + fb + fs + 1)
recall = tb / (tb + fs + 1)
print("Precision: ", precision)
print("Recall: ", recall)

f_measure = (2 * recall * precision) / (recall + precision + 1)
print("F-measure: ", f_measure)