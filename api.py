from flask import Flask, jsonify, send_from_directory

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
if __name__ == "__main__":
    app.run()
