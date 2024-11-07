from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Définissez les URLs des différents services
services = {
    "user_service": "http://user_service:5000",
    "movie_service": "http://movie_service:5000",
    "reco_service": "http://reco_service:5000",
    "list_service": "http://list_service:5000",
}

# Fonction pour rediriger les requêtes vers le bon service
def forward_request(service_url):
    response = requests.request(
        method=request.method,
        url=f"{service_url}{request.full_path}",
        headers={key: value for key, value in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    return (response.content, response.status_code, response.headers.items())

# Redirige /users vers user_service
@app.route('/users', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/users/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def user_service(path):
    return forward_request(services["user_service"])

# Redirige /movies vers movie_service
@app.route('/movies', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/movies/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def movie_service(path):
    return forward_request(services["movie_service"])

# Redirige /reco vers reco_service
@app.route('/reco', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/reco/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def reco_service(path):
    return forward_request(services["reco_service"])

# Redirige /lists vers list_service
@app.route('/lists', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/lists/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def list_service(path):
    return forward_request(services["list_service"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
