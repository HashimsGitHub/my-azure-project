import azure.functions as func
from azure.storage.fileshare import ShareServiceClient
from pymongo import MongoClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("imports OK", status_code=200)