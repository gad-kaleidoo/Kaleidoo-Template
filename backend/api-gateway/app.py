import os
import logging
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import custom modules
import manager
from permissions import Permission
from middleware import jwt_authenticated, sts_authenticated
from JsonFormatter import JsonFormatter
from werkzeug.routing import BaseConverter

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure all logging is captured by handlers, using JSON format for output
if not logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(JsonFormatter())
    logger.addHandler(stream_handler)
else:
    for handler in logger.handlers:
        handler.setFormatter(JsonFormatter())

# Custom converters for URL parameters
class IDConverter(BaseConverter):
    regex = '[0-9a-zA-Z]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

class NameConverter(BaseConverter):
    regex = '[a-zA-Z_]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

app.url_map.converters['id'] = IDConverter
app.url_map.converters['name'] = NameConverter

# API route definitions
@app.route("/api/<name:service>", methods=["POST"])
@app.route("/api/<name:service>/<name:action>", methods=["POST"])
@app.route("/api/product/<product>/<name:action>", methods=["POST"])
@app.route("/api/<name:service>/<name:action>/<name:type>", methods=["GET"])
@jwt_authenticated()
def manage_requests(service=None, action=None, type=None, product=None):
    user_d = Permission(request.uid).user
    logger.info("Processing request", extra={"user_id": user_d['user_id']})
    return jsonify(manager.process_request(service, action, type, product, request))

@app.route("/login/first_login", methods=["POST"])
@jwt_authenticated()
def first_login():
    user_info = Permission(request.uid).user
    logger.info("New user first login", extra={"user": user_info['user_name']})
    return jsonify(manager.initialize_user_session(user_info))

@app.get("/")
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 8080)), debug=os.getenv('DEBUG', 'False') == 'True')
