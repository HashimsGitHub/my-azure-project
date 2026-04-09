import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from pymongo import MongoClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID")
    
    # Connect to MongoDB
    client = MongoClient(os.environ["MONGODB_URI"])
    db = client.file_shares_db

    # Azure Provisioning
    cred = DefaultAzureCredential()
    storage_client = StorageManagementClient(cred, os.environ["AZURE_SUBSCRIPTION_ID"])
    
    share_name = f"share-{user_id[:6]}"
    
    try:
        storage_client.file_shares.create(
            "Your-Resource-Group", 
            "Your-Storage-Account", 
            share_name, 
            {"share_quota": 10}
        )
        # Log to MongoDB
        db.shares.insert_one({"user": user_id, "share": share_name})
        return func.HttpResponse("Created", status_code=201)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)