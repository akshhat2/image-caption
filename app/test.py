import pickle
from keras.applications.vgg16 import VGG16
from keras.models import load_model
model=load_model('app\\vgg16_weights_tf_dim_ordering_tf_kernels.h5')
# model = VGG16()