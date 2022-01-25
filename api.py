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
    return 'You\'re not supposed to be here...'

@app.route('/test', methods=["GET"])
def return_json():
    return jsonify({'test': True})

sarcasm_detector = SarcasmModel(path_to_build_folder="../sarcasm_nlp/", path_to_saved_model="../sarcasm_nlp/saved_model/fake_news_v1/")

@app.route('/sarcasm_detection', methods=["POST"])
def return_prediction():
    json_data = request.get_json()
    if (json_data is None):
        return jsonify({'error': 'api only accepts json format'})
    try:
        if ("query" in json_data):
            query = json_data["query"]
            if ("threshold" in json_data):
                try:
                    threshold = float(json_data["threshold"])
                    return jsonify(sarcasm_detector.predict(query, threshold))
                except ValueError:
                    return jsonify({'error': 'please pass in a float for threshold'})
            return jsonify(sarcasm_detector.predict(json_data["query"]))
        else: return jsonify({'error': 'please specify a string'})
    except: 
        return jsonify({'error': 'something went wrong'})


if __name__ == "__main__":
    app.run()
