import azure.functions as func
from azure.storage.fileshare import ShareServiceClient
from pymongo import MongoClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
    mongo_uri = os.environ.get("MONGODB_URI")
    return func.HttpResponse(f"conn={bool(conn_str)} mongo={bool(mongo_uri)}", status_code=200)