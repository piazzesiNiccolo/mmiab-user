import os
import base64
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import current_app
from mib.models import User

class Utils:

    def load_profile_picture(user : User) -> dict:
        file_name = user.pfp_path
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_name)
        print('path', file_path)
        try:
            with open(file_path, 'rb') as file:
                b64_file = base64.b64encode(file.read()).decode("utf8")
        except FileNotFoundError:
            print('not found')
            b64_file = ''

        return {
            'name': file_name,
            'data': b64_file,
            'type': os.path.splitext(file_name)[1][1:]
        }

    def save_profile_picture(propic: dict) -> str:
        if propic != '':
            b64_file = propic.get('data')
            bytes_file = base64.b64decode(b64_file.encode('utf-8'))
            file_name = str(uuid4()) + secure_filename(propic.get('name'))
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_name)
            with open(file_path, 'wb') as file:
                file.write(bytes_file)
            return file_name
        
        return ''


