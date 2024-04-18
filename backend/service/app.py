import threading
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from middleware import sts_authenticated  # Ensure middleware is properly implemented
from config import PORT
import service  # Changed from 'manager' to 'service' which should be defined accordingly
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route("/process/<workspace_id>/<org_id>", methods=["GET"])
@app.route("/process/<connection_id>/<workspace_id>/<org_id>", methods=["GET"])
def process_data(workspace_id, org_id, connection_id=None):
    """
    Generic endpoint to initiate a processing task based on workspace and optional connection specifics.
    """
    if org_id:
        try:
            # Retrieve connection data or handle without specific connection
            if connection_id:
                connection_data = service.get_connection_data(connection_id, org_id, workspace_id)
            else:
                connection_data = service.get_workspace_connection_data(org_id, workspace_id)

            logger.info(f"Connection data retrieved: {connection_data}")
            if 'Error' in connection_data:
                return jsonify({"Message": "Connection Error",
                                "Details": "Failed to configure source connection properly"}), 400
            
            org_details = service.get_organization_details(org_id)
            workspace_details = service.get_workspace_details(workspace_id, org_id)
            product_details = workspace_details["product_info"]
            bucket_name = org_details["storage_bucket_name"]

            # Validate workspace and product configuration
            if not service.is_destination_defined(workspace_id, org_id):
                return jsonify({"Message": "Configuration Error",
                                "Details": "Destination not configured in the project"}), 400
            if not workspace_details["is_product_defined"]:
                return jsonify({"Message": "Configuration Error",
                                "Details": f"{product_details['name']} not configured properly"}), 400

            # Processing logic based on connection type
            connection_type = connection_data["type"]
            processing_options = service.get_processing_options()

            processor = service.resolve_processor(connection_type, processing_options)
            if processor:
                folder_path = f"{workspace_id}/inbox"
                result = processor.process(workspace_id, org_id, folder_path, connection_data, bucket_name, product_details)
                
                if "success" in result:
                    threading.Thread(target=service.notify_product_system,
                                     args=(workspace_id, org_id, product_details['name'])).start()
                    del result["success"]
                if "Error" in result:
                    logger.error(f"Processing error: {result}")
                    return jsonify({"Message": "Processing Failed", "Details": result}), 500
                
                logger.info(f"Processing result: {result}")
                return jsonify({"Message": "Processing completed successfully", "Data": result}), 200
            else:
                return jsonify({"Message": "Processing Error",
                                "Details": f"No suitable processor found for type {connection_type}"}), 400
        except Exception as e:
            logger.error(f"Exception during processing: {str(e)}")
            return jsonify({"Message": "Server Error",
                            "Details": f"An error occurred: {str(e)}"}), 500
    return jsonify({"Message": "Input Error",
                    "Details": "Organization ID and Workspace ID are required"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
