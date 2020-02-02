import os
from flask import Flask, flash, request, redirect, url_for, jsonify,render_template

from werkzeug.utils import secure_filename
import cv2
import keras
import numpy as np
from keras.models import load_model
from keras import backend as K

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			image = cv2.imread(os.path.dirname(os.path.realpath(__file__))+"/uploads/"+filename)
			color_result = getDominantColor(image)
			result = findImg(image)
			redirect(url_for('upload_file',filename=filename))
			posts={'result': result,'color_result':color_result}
			return render_template('load.html',posts=posts)

	return render_template('home.html')

def findImg(image):
    '''Determines if the image taj_mahal_minar'''
    import cv2
    import numpy as np
    import keras
    from keras.models import load_model
    from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
    from keras.applications.resnet50 import preprocess_input, decode_predictions
    classifier = load_model('taj_mahal_minar.h5')
    #print(classifier.summary())
    classifier.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])
    
    # predicting images
    img = cv2.resize(image, (150,150), interpolation = cv2.INTER_AREA)
    #image = image.reshape(1,150,150,3) 
    #img = load_img(image, target_size=(150, 150))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    pred = classifier.predict(images)
    print(pred)
    
    #print('Predicted:', decode_predictions(pred, top=3)[0])
    validation_generator={'eiffel tower': 0, 'kutamb minar': 1, 'taj mahal': 2}
    j=0
    res=""
    for x, y in validation_generator.items():
      if(pred[0][j]==1):
          print(x, y)
          return x 
      j=j+1
    return res

def getDominantColor(image):
	'''returns the dominate color among Blue, Green and Reds in the image '''
	B, G, R = cv2.split(image)
	B, G, R = np.sum(B), np.sum(G), np.sum(R)
	color_sums = [B,G,R]
	color_values = {"0": "Blue", "1":"Green", "2": "Red"}
	return color_values[str(np.argmax(color_sums))]
	
if __name__ == "__main__":
	app.run(host= '0.0.0.0', port=80)


