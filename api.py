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

sarcasm_detector = SarcasmModel(path_to_build_folder="../sarcasm_nlp/", path_to_saved_model="../sarcasm_nlp/saved_model2/fake_news_v1/")

@app.route('/sarcasm_iteration', methods=["POST"])
def commit_iteration():
    try:
        sarcasm_detector.additional_train_model()
        return jsonify({"success": True});
    except Exception as e:
        return jsonify({'success': False, 'error': e});

@app.route('/sarcasm_reset', methods=["POST"])
def commit_reset():
    try:
        global sarcasm_detector 
        sarcasm_detector = SarcasmModel(path_to_build_folder="../sarcasm_nlp/", path_to_saved_model="../sarcasm_nlp/saved_model2/fake_news_v1/")
        return jsonify({"success": True});
    except Exception as e:
        return jsonify({'success': False, 'error': e});


@app.route('/sarcasm_detection', methods=["POST"])
def return_prediction():
    json_data = request.get_json()
    if (json_data is None):
        return jsonify({'error': 'api only accepts json format'})
    try:
        if ("queries" in json_data):
            entries = json_data["queries"]
            if ("threshold" in json_data):
                try:
                    threshold = float(json_data["threshold"])
                    return jsonify(sarcasm_detector.predict(entries, threshold))
                except ValueError:
                    return jsonify({'error': 'please pass in a float for threshold'})
            return jsonify(sarcasm_detector.predict(entries))

        if ("query" in json_data):
            query = json_data["query"]
            if ("threshold" in json_data):
                try:
                    threshold = float(json_data["threshold"])
                    return jsonify(sarcasm_detector.predict(query, threshold))
                except ValueError:
                    return jsonify({'error': 'please pass in a float for threshold'})
            return jsonify(sarcasm_detector.predict(query))
        else: return jsonify({'error': 'please specify a string'})
    except Exception as e:
        return jsonify({'error': f'{e}'})


if __name__ == "__main__":
    app.run()
