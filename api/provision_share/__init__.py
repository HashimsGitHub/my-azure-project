import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING", "NOT SET")
    
    # Don't expose the full string, just check its structure
    has_account_name = "AccountName=" in conn_str
    has_account_key = "AccountKey=" in conn_str
    has_endpoint = "EndpointSuffix=" in conn_str
    length = len(conn_str)
    
    return func.HttpResponse(
        f"length={length} AccountName={has_account_name} AccountKey={has_account_key} EndpointSuffix={has_endpoint}",
        status_code=200
    )