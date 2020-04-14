from flask import *
from werkzeug.wrappers import Request, Response
from werkzeug.utils import secure_filename
import os
from flask_caching import Cache
import predict

app = Flask(__name__) 
i=1
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0.002

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/') 
def test(): 
    return render_template('test.html') 
@app.route('/next') 
def next(): 
    return render_template('next.html')
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    resp=Response()
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    if request.method == 'POST':
        f= request.files['pic']
        print(f)
        print(request.files)
        # f.save(secure_filename("temp.jpg"))

        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        try:
            os.remove(os.path.join(THIS_FOLDER,'static','css','temp5.jpg'))
        except:
            print("No file")
        f.save(os.path.join(THIS_FOLDER,'static','css',secure_filename("temp5.jpg")))
        message=(predict.predict(f)+".").capitalize()
        print(message)
        # message=message.capitalize()    
        # f.save("/static/"+f.filename)
        print(THIS_FOLDER)
    return render_template("next.html",message=message,ttt=os.path.join(THIS_FOLDER,'static','css','temp5.jpg'))
# @app.route('/about/') def about(): return render_template('about.html') 
if __name__ == '__main__': 
    app.run(debug=True)