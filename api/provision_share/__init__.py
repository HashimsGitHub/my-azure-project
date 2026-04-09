import azure.functions as func
import os
from azure.storage.fileshare import ShareServiceClient
from pymongo import MongoClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    # 1. Identity from SWA Header
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID", "anonymous")
    
    # 2. Get Secrets from App Settings
    conn_str = os.environ["STORAGE_CONNECTION_STRING"]
    mongo_uri = os.environ["MONGODB_URI"]

    try:
        # 3. Create Azure File Share
        service_client = ShareServiceClient.from_connection_string(conn_str)
        share_name = f"fs-{user_id[:6]}"
        share_client = service_client.get_share_client(share_name)
        
        # Create share with 5GB quota for the prototype
        share_client.create_share(quota=5)

        # 4. Log to MongoDB
        mongo_client = MongoClient(mongo_uri)
        db = mongo_client.get_default_database()
        db.shares.update_one(
            {"user_id": user_id},
            {"$set": {"share_name": share_name, "status": "provisioned"}},
            upsert=True
        )

        return func.HttpResponse(f"Successfully created share: {share_name}", status_code=201)
    except Exception as e:
        return func.HttpResponse(f"Provisioning failed: {str(e)}", status_code=500)