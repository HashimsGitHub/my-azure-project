import azure.functions as func
import os
from azure.storage.fileshare import ShareServiceClient
from azure.core.exceptions import ResourceExistsError

def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID", "tester")

    try:
        # 1. Clean the name
        clean_id = "".join(filter(str.isalnum, user_id.lower()))
        share_name = f"fs-{clean_id[:10]}"
        
        # 2. Initialize client
        service_client = ShareServiceClient.from_connection_string(conn_str)
        share_client = service_client.get_share_client(share_name)
        
        # 3. Try to create, but catch if it already exists
        try:
            share_client.create_share(quota=5)
            message = "Share created successfully."
        except ResourceExistsError:
            message = "Share already exists, skipping creation."

        return func.HttpResponse(message, status_code=200)

    except Exception as e:
        # This will tell us if it's a 'Connection String' error vs a 'Library' error
        return func.HttpResponse(f"Actual Error: {str(e)}", status_code=500)