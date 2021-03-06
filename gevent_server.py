from gevent.pywsgi import WSGIServer
from flask import Flask, request, abort, jsonify, send_from_directory
import os

UPLOAD_DIRECTORY = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "www")
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

app = Flask(__name__)

@app.route("/firmware")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route("/firmware/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

@app.route("/firmware/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201

@app.route('/')
def index():
    return 'Firmware OTA Server'

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app,
        keyfile='ca_key.pem', certfile='ca_cert.pem')
    http_server.serve_forever()
