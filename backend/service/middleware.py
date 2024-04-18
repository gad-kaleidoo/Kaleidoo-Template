import threading
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from middleware import sts_authenticated
from config import PORT
import manager
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


@app.route("/scan/<workspace_id>/<org_id>", methods=["GET"])
@app.route("/scan/<conn_id>/<workspace_id>/<org_id>", methods=["GET"])
def scan_documents(workspace_id, conn_id=None, org_id=None):
    if org_id:
        try:
            if conn_id:
                res = manager.get_connection_data(conn_id, org_id, workspace_id)
            else:
                res = manager.get_workspace_connection_data(org_id, workspace_id)
            logger.info(f"response from get workspace connection: {res}")
            if 'Error' in res:
                return jsonify({"Message": "Error while getting workspace connection",
                                "Error": "cannot start scanning without source connection configured in the project"}), 400
            org = manager.get_organization(org_id)
            workspace = manager.get_workspace(workspace_id=workspace_id, org_id=org_id)["data"]
            product = workspace["product"]
            bucket_name = org["bucket_name"]
            if not manager.defined_workspace_dest(workspace_id, org_id):
                return jsonify({"message": "Error while getting workspace connection",
                                "Error": "cannot start scanning without destination configured in the project"}), 400
            if not workspace["product_defined"]:
                return jsonify({"Message": "Error while getting workspace connection",
                                "Error": f"cannot start scanning without {product} details defined for that project"}), 400
            connection = res
            if connection:
                res = manager.get_connection_options()
                if "Error" in res:
                    logger.error(res)
                    return jsonify({"Message": "Error while getting connection options", "Error": res}), 400
                options = res["types"]
                handle_manager = None
                for item in options:
                    for key in item:
                        if connection["type"] == key:
                            handle_manager = key
                            break
                        if isinstance(item[key], list):
                            if connection["type"] in item[key]:
                                handle_manager = key
                                break

                scan_manager = manager.handle_managers(handle_manager)
                folder_path = f"{workspace_id}/inbox"
                if scan_manager:
                    logger.info("start scanning")
                    result = scan_manager.scan(workspace_id, org_id, folder_path, connection, bucket_name, product)
                    if "success" in result:
                        thread = threading.Thread(target=manager.send_trigger_to_product,
                                                  args=(workspace_id, str(org["_id"]), product))
                        thread.start()
                        del result["success"]
                    if "Error" in result:
                        logger.error(result)
                        return jsonify({"Message": "Error while scanning the documents", "Error": result}), 500
                    if "Exception Error" in result:
                        logger.error(result)
                        return jsonify({"Message": "Error while scanning the documents", "Error": result}), 500
                    logger.info(result)
                    return jsonify({"Message": "Scanning completed successfully", "Data": result}), 200
                else:
                    return jsonify({"Message": "Error while scanning the documents",
                                    "Error": f"there is no type {handle_manager} in the list"}), 400
            else:
                return jsonify({"Message": "Error while scanning the documents",
                                "Error": f"there is no connection with id {conn_id}"}), 400
        except Exception as e:
            return jsonify({"Message": "Error while scanning the documents",
                            "Exception Error": f"error while scanning the documents: {str(e)}"}), 500
    return jsonify({"Message": "Error while scanning the documents",
                    "Error": "connection id and organization id are required"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
