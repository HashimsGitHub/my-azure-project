import azure.functions as func
import os
from azure.storage.fileshare import ShareServiceClient
from azure.core.exceptions import ResourceExistsError

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("storage imports OK", status_code=200)