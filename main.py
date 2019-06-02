from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_cors import CORS
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

CORS(app)

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'Daniel' or password != 'Password':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/overview', methods=['GET'])
@jwt_required
def fetchOverview():
    try:
        ow = open('current_overview.md', 'r')
        markdown = ow.read()
        ow.close()
    except FileNotFoundError:
        markdown = "# No overview found"

    return jsonify({"markdown":markdown}), 200

@app.route('/overview', methods=['POST'])
@jwt_required
def saveOverview():
    data = request.get_json()
    ow = open('current_overview.md', 'w+')
    ow.write(data)
    ow.close()

    return jsonify({"msg": "Overview saved"}), 200

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"msg": "Overview saved"}), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, threaded=True)