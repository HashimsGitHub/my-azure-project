import azure.functions as func
import os
import traceback
from azure.storage.fileshare import ShareServiceClient
from pymongo import MongoClient
from azure.core.exceptions import ResourceExistsError

def main(req: func.HttpRequest) -> func.HttpResponse:
    # 1. Capture Inputs
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
    mongo_uri = os.environ.get("MONGODB_URI")
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID", "internal_tester")

    try:
        # 2. Storage Logic
        if not conn_str:
            return func.HttpResponse("Error: STORAGE_CONNECTION_STRING is missing in Azure Settings", status_code=500)
            
        # Ensure name is valid: lowercase, alphanumeric, at least 3 chars
        clean_id = "".join(filter(str.isalnum, user_id.lower()))
        share_name = f"fs-{clean_id[:10]}" if len(clean_id) > 0 else "fs-default-user"
        
        service_client = ShareServiceClient.from_connection_string(conn_str)
        share_client = service_client.get_share_client(share_name)
        
        try:
            share_client.create_share(quota=5)
        except ResourceExistsError:
            pass # This is fine, we just continue

        # 3. MongoDB Logic (Wrapped in its own try/except so it doesn't kill the whole process)
        if mongo_uri:
            try:
                # Adding a timeout so it doesn't hang the function
                client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
                db = client["smb_app_db"] 
                db.shares.update_one(
                    {"user_id": user_id},
                    {"$set": {"share_name": share_name, "status": "active"}},
                    upsert=True
                )
            except Exception as mongo_err:
                # If MongoDB fails, we still want the user to know the SHARE was created
                return func.HttpResponse(f"Share created, but MongoDB failed: {str(mongo_err)}", status_code=201)

        return func.HttpResponse(f"Success: {share_name} is ready.", status_code=201)

    except Exception as e:
        # This is the "Gold Mine" of info. 
        # It will print the exact line number and error type.
        error_msg = traceback.format_exc()
        return func.HttpResponse(f"Python Crash Report:\n{error_msg}", status_code=500)