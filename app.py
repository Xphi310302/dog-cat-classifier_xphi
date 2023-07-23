import streamlit as st
from tensorflow.keras.models import load_model  # TensorFlow is required for Keras to work
# from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import tensorflow.keras.backend as K  
import cv2

np.set_printoptions(suppress=True)
K.clear_session()

# Load the model
model = load_model("converted_keras/keras_model.h5", compile=False)
class_names = ['cat', 'dog']

def preprocess_image(image):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # size = (224, 224)
    # image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image = cv2.resize(image, (224, 224))
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    return data

st.title('Cat And Dog Classifier')
st.markdown("***")

st.subheader("Upload the image of cat or dog")
option = st.radio('',('Single image', 'Multiple image'))
st.write('You selected:', option)

if option == 'Single image':
    uploaded_file = st.file_uploader(' ',accept_multiple_files = False, label_visibility = "hidden")

    if uploaded_file is not None:   
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        preprocessed_image = preprocess_image(opencv_image)
        pred_label = np.argmax(model.predict(preprocessed_image))
        # pred_label = labels(np.argmax(loaded_model.predict(preprocessed_image)))
        print(uploaded_file.name)
        st.image(uploaded_file)
        st.subheader(class_names[pred_label])

elif option == 'Multiple image':
    uploaded_file = st.file_uploader(' ',accept_multiple_files = True)
    if uploaded_file is not None:   
        if len(uploaded_file) != 0:
            st.write("Images Uploaded Successfully")
            # Perform your Manupilations (In my Case applying Filters)
            for i in range(len(uploaded_file)):
                file_bytes = np.asarray(bytearray(uploaded_file[i].read()), dtype=np.uint8)
                # opencv_image = cv2.imdecode(file_bytes, 1)
                
                # pred_mask = predict(opencv_image, model, False)
                # st.image(uploaded_file[i])
                # st.image(pred_mask)
                opencv_image = cv2.imdecode(file_bytes, 1)
                preprocessed_image = preprocess_image(opencv_image)
                pred_label = np.argmax(model.predict(preprocessed_image))
                # pred_label = labels(np.argmax(loaded_model.predict(preprocessed_image)))
                print(uploaded_file[i].name)
                st.image(uploaded_file[i])
                st.subheader(class_names[pred_label])

            
else:
    st.write("Make sure you image is in TIF/JPG/PNG Format.")