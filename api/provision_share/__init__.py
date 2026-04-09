import azure.functions as func
import os
import traceback
from azure.storage.fileshare import ShareServiceClient
from pymongo import MongoClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    # 1. Get credentials from environment variables
    # (Ensure these are set in your SWA Configuration in the Portal)
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
    mongo_uri = os.environ.get("MONGODB_URI")
    
    # Get user identity from Azure SWA header
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID", "anon_user")

    try:
        # 2. Azure Share Creation
        # Clean the user_id for Azure naming standards (lowercase, alphanumeric)
        clean_id = "".join(filter(str.isalnum, user_id.lower()))
        share_name = f"fs-{clean_id[:10]}"
        
        # We use from_connection_string because it automatically knows 
        # which Storage Account to talk to!
        service_client = ShareServiceClient.from_connection_string(conn_str)
        share_client = service_client.get_share_client(share_name)
        
        # Create the share (quota is in GB)
        share_client.create_share(quota=5)

        # 3. MongoDB Log (Optional but good for your records)
        if mongo_uri:
            client = MongoClient(mongo_uri)
            # This gets the DB name from the URI itself
            db = client.get_default_database()
            db.shares.update_one(
                {"user_id": user_id},
                {"$set": {"share_name": share_name, "status": "active"}},
                upsert=True
            )

        return func.HttpResponse("Share created successfully", status_code=201)

    except Exception as e:
        # If it fails, this helps us see exactly why in the browser
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)