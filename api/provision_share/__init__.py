import os
from azure.storage.file_share import ShareServiceClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID")
    connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    
    try:
        # Create the client using the Connection String
        service_client = ShareServiceClient.from_connection_string(connection_string)
        
        share_name = f"share-{user_id[:6]}"
        share_client = service_client.get_share_client(share_name)
        
        # Create the share
        share_client.create_share(quota=10) # 10GB for prototype
        
        return func.HttpResponse("Share created successfully!", status_code=201)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)