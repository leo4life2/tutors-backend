from flask import Blueprint, json
import logging

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload():
    return json.jsonify({'message': "upload success"}), 200