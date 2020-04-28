# Example Controllers
from app import app
from flask import render_template, redirect, url_for
# from app.models.Hello import Hello
# ///
# Import models
# from app.models.Hello import Hello
# ///
#route index
@app.route('/', methods = ['GET'])
def index():
    data = {
        "title": "Hello World",
        "body": "Flask MVC :)"
    }

    # Hello.insert_data()
    
    return render_template('index.html', data = data)