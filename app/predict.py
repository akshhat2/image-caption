from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model
from pickle import load
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def generate_desc(model, tokenizer, photo, max_length):
    
# seed the generation process
    in_text = 'startseq'
    # iterate over the whole length of the sequence
    for i in range(max_length):
        
        # integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # predict next word
        yhat = model.predict([photo,sequence], verbose=0)
        # convert probability to integer
        yhat = argmax(yhat)
        # map integer to word
        word = word_for_id(yhat, tokenizer)
        # stop if we cannot map the word
        if word is None:
            break
        # append as input for generating the next word
        in_text += ' ' + word
        # stop if we predict the end of the sequence
        if word == 'endseq':
            break
    return in_text
 
# extract features from each photo in the directory
def extract_features(filename):
    
  # load the model
    # model = load_model('app\\vgg16_weights_tf_dim_ordering_tf_kernels.h5')
    model = VGG16()
  # re-structure the model
    model.layers.pop()
    model = Model(inputs=model.inputs, outputs=model.layers[-1].output)
  # load the photo
    image = load_img(filename, target_size=(224, 224))
  # convert the image pixels to a numpy array
    image = img_to_array(image)
  # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
	# prepare the image for the VGG model
    image = preprocess_input(image)
  # get features
    feature = model.predict(image, verbose=0)
    del model
    return feature
 
# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None
 
# load the tokenizer
def predict(fname):

  tokenizer = load(open('app\\tokenizer.pkl', 'rb'))
  # pre-define the max sequence length (from training)
  max_length = 34
  # load the model
  model = load_model('app\\models\\model-ep014-loss3.413-val_loss3.656.h5')
  # load and prepare the photograph

  photo = extract_features(fname)
  
  # generate description
  description = generate_desc(model, tokenizer, photo, max_length)
  return description[9:-6]
    # img=mpimg.imread(fname)
    # imgplot = plt.imshow(img)
    # plt.axis('off')

    # plt.show()
# del model