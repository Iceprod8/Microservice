from flask import Flask, request
import requests
import os
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback_secret_key')
app.config['SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)

# Définissez les URLs des différents services
services = {
    "user_service": "http://user_service:5000",
    "movie_service": "http://movie_service:5000",
    "reco_service": "http://reco_service:5000",
    "list_service": "http://list_service:5000",
}

# Fonction pour rediriger les requêtes vers le bon service
def forward_request(service_url, add_user_header=False):
    headers = {key: value for key, value in request.headers}
    
    if add_user_header:
        current_user = get_jwt_identity()
        headers["X-User-ID"] = str(current_user)

    response = requests.request(
        method=request.method,
        url=f"{service_url}{request.full_path}",
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    return (response.content, response.status_code, response.headers.items())

# Routes vers les différents services
@app.route('/users', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/users/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def user_service(path):
    return forward_request(services["user_service"])

@app.route('/movies', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/movies/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required()
def movie_service(path=""):
    return forward_request(services["movie_service"], add_user_header=True)

@app.route('/reco', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/reco/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required()
def reco_service(path=""):
    return forward_request(services["reco_service"], add_user_header=True)

@app.route('/lists', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/lists/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required()
def list_service(path=""):
    return forward_request(services["list_service"], add_user_header=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)