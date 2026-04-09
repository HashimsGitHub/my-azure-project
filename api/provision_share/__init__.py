import azure.functions as func
import os
import traceback
from azure.storage.fileshare import ShareServiceClient
from azure.core.exceptions import ResourceExistsError
from pymongo import MongoClient

import base64

STORAGE_KEY_B64 = "ZFdudHJ6SFE3aFR2ZUgrQ3N0VFRjMTNtKy9RQzlQa2tQVVBNN3BkUGNvVFhVQ0M2alRVNjRzOHIyck11eURYOXZuYW4yQkZtajlVcytBU3RZRkZhQkc9PQ=="
STORAGE_KEY = base64.b64decode(STORAGE_KEY_B64).decode("utf-8")

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

        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            db = client["file_shares_db"]
            db.shares.update_one(
                {"user_id": user_id},
                {"$set": {"share_name": share_name}},
                upsert=True
            )
        except Exception as db_err:
            return func.HttpResponse(
                f"Share created but DB log failed: {str(db_err)}|{share_name}|{STORAGE_KEY}",
                status_code=201
            )

        return func.HttpResponse(
            f"Success: share '{share_name}' created and DB updated.|{share_name}|{STORAGE_KEY}",
            status_code=201
        )

    except Exception:
        return func.HttpResponse(traceback.format_exc(), status_code=500)