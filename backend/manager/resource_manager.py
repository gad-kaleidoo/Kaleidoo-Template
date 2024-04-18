import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from manager.validators import ResourceSchema  # Corrected import path
from manager.resource_manager import ResourceManager  # Corrected import path
from jsonFormatter import JsonFormatter
import sys

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize ResourceManager
resource_manager = ResourceManager()

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
if not logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(JsonFormatter())
    logger.addHandler(stream_handler)

# API endpoint to handle all CRUD operations for resources
@app.route('/resource/<string:organization_id>/<workspace_id>', methods=['POST', 'GET'])
@app.route('/resource/<string:organization_id>/<workspace_id>/<string:resource_id>', methods=['GET', 'PUT', 'DELETE'])
def resource(organization_id, workspace_id, resource_id=None):
    try:
        if request.method == 'POST':
            # Create a new resource
            data = request.get_json()
            errors = ResourceSchema().validate(data)
            if errors:
                logger.error(f"Validation errors: {errors}")
                return jsonify({"Message": "Validation Error", "Errors": errors}), 400
            response = resource_manager.add_resource(data, organization_id, workspace_id)
            return jsonify(response), 201 if response.get('status') == 'success' else 400

        elif request.method == 'GET':
            if resource_id:
                # Retrieve a specific resource
                response = resource_manager.get_resource(resource_id, organization_id, workspace_id)
                return jsonify(response), 200 if response else 404
            else:
                # Retrieve all resources
                response = resource_manager.get_all_resources(organization_id, workspace_id)
                return jsonify(response), 200 if response else 404

        elif request.method == 'PUT':
            # Update a specific resource
            data = request.get_json()
            response = resource_manager.update_resource(data, resource_id, organization_id, workspace_id)
            return jsonify(response), 200 if response.get('status') == 'success' else 400

        elif request.method == 'DELETE':
            # Delete a specific resource
            response = resource_manager.delete_resource(resource_id, organization_id, workspace_id)
            return jsonify(response), 200 if response.get('status') == 'success' else 404
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({"Message": "Server error", "Error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Default to 5000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=True)
