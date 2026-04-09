import azure.functions as func
import os
import traceback
from azure.storage.fileshare import ShareServiceClient
from azure.core.exceptions import ResourceExistsError
from pymongo import MongoClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
    mongo_uri = os.environ.get("MONGODB_URI")
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID", "tester_user")

    try:
        clean_id = "".join(filter(str.isalnum, user_id.lower()))
        share_name = f"fs-{clean_id[:10]}"

        service_client = ShareServiceClient.from_connection_string(conn_str)
        share_client = service_client.get_share_client(share_name)

        try:
            share_client.create_share(quota=5)
        except ResourceExistsError:
            pass

        return func.HttpResponse(f"Stage 1 OK: share '{share_name}' created", status_code=200)

    except Exception:
        return func.HttpResponse(f"Stage 1 FAILED:\n{traceback.format_exc()}", status_code=500)