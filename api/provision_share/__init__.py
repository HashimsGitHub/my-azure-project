import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("provision_share alive", status_code=200)