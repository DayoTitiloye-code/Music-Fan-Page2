from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import render_template
from werkzeug import exceptions

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"message": f"Sorry... {err}"}), 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"message": f"It's not you, it's us"}), 500

if __name__ == '__main__':
    app.run()


