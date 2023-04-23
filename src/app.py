import os
from flask import Flask
from flask_cors import CORS
from src.apis.upload import upload_bp
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(upload_bp)
app.secret_key = os.urandom(24)

@app.route('/ping')
def pingpong():
    return 'pong'

if __name__ == '__main__':
    app.run(debug=True)