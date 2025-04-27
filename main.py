import os
import json
import base64
import requests
from Crypto.PublicKey import RSA
from urllib.parse import quote_plus
from Crypto.Util.Padding import unpad
from decrypt_manager import DecryptManager
from Crypto.Cipher import AES, PKCS1_OAEP
from flask import Flask, request, jsonify, redirect, Blueprint, render_template

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'template'))
portability_bp = Blueprint("portability_bp", __name__, url_prefix="/portability")
decrypt_manager = DecryptManager()

@portability_bp.route('/', methods=['GET'])
def portability():
    return render_template('portability.html')


@portability_bp.route('/get-data', methods=['GET'])
def test_portability():
    public_key_string = decrypt_manager.get_key(decrypt_manager.path_to_public_key, key_str=True)
    public_key = quote_plus(public_key_string)
    callback = 'http://localhost:5080/portability/show-data'
    return redirect(f'http://127.0.0.1:5000/portability/?callback={callback}&public_key={public_key}', code=302)


@portability_bp.route('/show-data', methods=['GET'])
def callback():
    encrypt_data = request.args.get('data')
    decrypt_data = decrypt_manager.decrypt_data(encrypt_data)
    return {'encrypt data': encrypt_data, 'decrypt data': decrypt_data}


app.register_blueprint(portability_bp)


@app.route('/', methods=['GET'])
def root():
    return redirect('/portability', code=301)

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return redirect('/portability', code=301)

@app.route('/portability/<path:path>', methods=['GET', 'POST'])
def catch_all_portability(path):
    return redirect('/portability', code=301)

if __name__ == '__main__':
    app.run(host='localhost', port=5080, debug=True)
