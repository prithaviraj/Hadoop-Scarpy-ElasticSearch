
# In[4]: # #### Loading out saved history is as simple as these two lines
import pickle 

pickle_in = open("MNIST_history2.pickle","rb")
saved_history = pickle.load(pickle_in)
print(saved_history)



# ### Displaying our Confusion Matrix


# In[24]:  # ### Testing our Classifier


import cv2
import numpy as np
import keras
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
classifier = load_model('taj_mahal_minar2222.h5')
print(classifier.summary())
classifier.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# In[2]:

# predicting images
img = load_img('minar.jpg', target_size=(150, 150))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)
images = np.vstack([x])
pred = classifier.predict(images)
print(pred)
from keras.applications.resnet50 import preprocess_input, decode_predictions
#print('Predicted:', decode_predictions(pred, top=3)[0])
validation_generator={'eiffel tower': 0, 'kutamb minar': 1, 'taj mahal': 2}
j=0
for x, y in validation_generator.items():
  if(pred[0][j]==1):
      print(x, y)
      break 
  j=j+1
#classes = train_generator.class_indices