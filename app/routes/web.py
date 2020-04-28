from app import app

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/json')
def main():
    return "json"