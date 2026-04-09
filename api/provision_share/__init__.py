import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Test 1: Can we import the storage package?
    try:
        from azure.storage.fileshare import ShareServiceClient
    except Exception as e:
        return func.HttpResponse(f"FAIL import ShareServiceClient: {str(e)}", status_code=500)

    # Test 2: Can we import pymongo?
    try:
        from pymongo import MongoClient
    except Exception as e:
        return func.HttpResponse(f"FAIL import MongoClient: {str(e)}", status_code=500)

    # Test 3: Can we read env vars?
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
    mongo_uri = os.environ.get("MONGODB_URI")
    if not conn_str:
        return func.HttpResponse("FAIL: STORAGE_CONNECTION_STRING is None", status_code=500)
    if not mongo_uri:
        return func.HttpResponse("FAIL: MONGODB_URI is None", status_code=500)

    # Test 4: Can we connect to Storage?
    try:
        svc = ShareServiceClient.from_connection_string(conn_str)
        shares = list(svc.list_shares())
        share_names = [s['name'] for s in shares]
    except Exception as e:
        return func.HttpResponse(f"FAIL Storage connect: {str(e)}", status_code=500)

    # Test 5: Can we connect to MongoDB?
    try:
        from pymongo import MongoClient
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
    except Exception as e:
        return func.HttpResponse(f"FAIL MongoDB connect: {str(e)}", status_code=500)

    return func.HttpResponse(f"ALL OK. Shares found: {share_names}", status_code=200)