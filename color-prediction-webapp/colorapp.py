import os
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

# Load the trained model
model = load_model('trainedmodels.h5')

# Define a dictionary to map class indices to color names
color_mapping = {
    0: 'Black',
    1: 'Blue',
    2: 'Brown',
    3: 'Green',
    4: 'Grey',
    5: 'Red',
    6: 'White',
    7: 'Yellow'
}

# Preprocess the input image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.0  # Rescale image to match training data preprocessing
    return img

@app.route('/', methods=['GET', 'POST'])
def upload_predict():
    if request.method == 'POST':
        # Get the uploaded file from the request
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            # Save the uploaded file temporarily
            temp_path = 'temp.jpg'
            uploaded_file.save(temp_path)

            # Preprocess the uploaded image
            input_img = preprocess_image(temp_path)

            # Make predictions using the model
            predictions = model.predict(input_img)

            # Get the index of the predicted class
            predicted_class_idx = np.argmax(predictions)

            # Get the predicted color name using the color_mapping dictionary
            predicted_color = color_mapping.get(predicted_class_idx, 'Not matched with any color')

            # Remove the temporary uploaded file
            os.remove(temp_path)

            return render_template('result.html', color=predicted_color)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
