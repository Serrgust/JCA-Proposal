from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins ='*')

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(
        {
            "users": ['Reynaldo',   # List of users
                      'Jorge', 
                      'Edgar', 
                      'Alessandra']
        }
    )

if __name__ == "__main__": 
    app.run(debug=True)