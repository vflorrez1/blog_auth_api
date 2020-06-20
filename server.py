from flask import Flask, jsonify, Response, request, json
from sql import read_sql
from config import secret, allowed_origin
import jwt

app = Flask(__name__)


@app.route('/is_authenticated', methods=['GET'])
def read_cookie():
    resp = Response(mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = allowed_origin
    resp.headers['Access-Control-Allow-Credentials'] = 'true'

    encoded_jwt = request.cookies.get('jwt')
    if encoded_jwt:
        try:
            jwt.decode(encoded_jwt, secret, algorithm='HS256')
            resp.response = json.dumps({'authenticated': True})
        except:
            resp.response = json.dumps({'authenticated': False})
    return resp


@app.route('/post_cred', methods=['POST', 'OPTIONS'])
def post_credentials():
    resp = Response(mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = allowed_origin
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    allowed_headers = 'Access-Control-Allow-Origin, Access-Control-Allow-Credentials, Content-Type'
    resp.headers['Access-Control-Allow-Headers'] = allowed_headers

    if request.method == 'POST':
        body = request.json
        email = body['email']
        password = body['password']
        query_string = "SELECT * FROM TestDb1.TestTable1 WHERE Name = '{}' AND Password = '{}'".format(email, password)
        data = read_sql(query_string)
        if not data.empty:
            encoded_jwt = jwt.encode(body, secret, algorithm='HS256')
            resp.set_cookie(key='jwt', value=encoded_jwt, secure=False, httponly=True, domain='127.0.0.1')
            resp.response = json.dumps({'authenticated': True})
            return resp

    resp.response = json.dumps({'authenticated': False})
    return resp


if __name__ == '__main__':
    app.run(debug=True)


