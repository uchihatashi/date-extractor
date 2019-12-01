from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from single_img_function import *
app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        pre_date, dates = my_main(filename)
        return "<h3>date on receipt = "+ pre_date + " converted date = " + dates + "</h3>"

    return render_template('upload.html')


if __name__ == '__main__':
	app.run(port=8080, debug=True)