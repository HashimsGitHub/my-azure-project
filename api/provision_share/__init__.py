import azure.functions as func
import os
import traceback
from azure.storage.fileshare import ShareServiceClient
from pymongo import MongoClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
    mongo_uri = os.environ.get("MONGODB_URI")
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID", "tester_user")

    try:
        # --- STAGE 1: AZURE STORAGE (Priority) ---
        clean_id = "".join(filter(str.isalnum, user_id.lower()))
        share_name = f"fs-{clean_id[:10]}"
        
        service_client = ShareServiceClient.from_connection_string(conn_str)
        share_client = service_client.get_share_client(share_name)
        
        try:
            share_client.create_share(quota=5)
        except Exception as e:
            if "ResourceExistsError" not in str(e):
                raise e

        # --- STAGE 2: MONGODB (Isolated) ---
        try:
            # Set a very short timeout (3 seconds) so the function doesn't hang
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            db = client.get_default_database()
            db.shares.update_one(
                {"user_id": user_id},
                {"$set": {"share_name": share_name}},
                upsert=True
            )
        except Exception as db_err:
            # If DB fails, we return a 201 because the STORAGE share was still created!
            return func.HttpResponse(f"Share created, but DB log failed: {str(db_err)}", status_code=201)

        return func.HttpResponse("Success: Share and DB updated.", status_code=201)

    except Exception:
        # If we hit this, the error is in the STORAGE part or logic
        return func.HttpResponse(traceback.format_exc(), status_code=500)