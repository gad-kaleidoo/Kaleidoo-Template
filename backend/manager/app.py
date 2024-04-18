import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import PORT
from backend.manager.validators import ResourceSchema  # Generic schema name
from manager import resource_manager  # Generic manager module name
from jsonFormatter import JsonFormatter
import sys

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if not logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(JsonFormatter())
    logger.addHandler(stream_handler)

# Generic endpoint to handle all CRUD operations for a resource
@app.route('/resource/<string:organization_id>/<workspace_id>', methods=['POST', 'GET'])
@app.route('/resource/<string:organization_id>/<workspace_id>/<string:resource_id>', methods=['GET', 'PUT', 'DELETE'])
def resource(organization_id, workspace_id, resource_id=None):
    if request.method == 'POST':
        # Create a new resource
        data = request.get_json()
        errors = ResourceSchema().validate(data)
        if errors:
            logger.error(resource_manager.format_errors(errors))
            return jsonify({"Message": "Validation Error", "Errors": errors}), 400
        response = resource_manager.add_resource(data, organization_id, workspace_id)
        return jsonify(response), 201 if response.get('status') == 'success' else 400

    elif request.method == 'GET':
        if resource_id:
            # Get a specific resource
            response = resource_manager.get_resource(resource_id, organization_id, workspace_id)
            return jsonify(response), 200 if response else 404
        else:
            # Get all resources
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
