from flask import Flask, jsonify, send_from_directory, request, Response
import sys
sys.path.append('../')
from sarcasm_nlp.sarcasm_model import SarcasmModel

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return (send_from_directory("./assets", 'favicon.ico'))

@app.route('/')
def homepage():
    return '<h3>You\'re not supposed to be here...</h3>'

@app.route('/test', methods=["GET"])
def return_json():
    return jsonify({'test': True})

sarcasm_detector = SarcasmModel(path_to_build_folder="../sarcasm_nlp/", path_to_saved_model="../sarcasm_nlp/saved_model/fake_news_v1/")

@app.route('/sarcasm_detection', methods=["POST"])
def return_prediction():
    json_data = request.get_json()
    if (json_data["query"]):
        return jsonify(sarcasm_detector.predict(json_data["query"]))
    else: return jsonify({'error': 'please specify a string'});

if __name__ == "__main__":
    app.run()
