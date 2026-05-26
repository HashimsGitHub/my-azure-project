import azure.functions as func
import os
import json
import base64
import traceback
from azure.storage.fileshare import ShareServiceClient
from azure.core.exceptions import ResourceExistsError
from pymongo import MongoClient


def get_github_claims(req):
    """Decode the SWA X-MS-CLIENT-PRINCIPAL header to extract GitHub identity claims."""
    principal_header = req.headers.get("X-MS-CLIENT-PRINCIPAL", "")
    if not principal_header:
        return {}, "unknown"
    try:
        decoded = base64.b64decode(principal_header).decode("utf-8")
        principal = json.loads(decoded)
        claims = {c["typ"]: c["val"] for c in principal.get("claims", [])}
        return claims, principal.get("userDetails", "unknown")
    except Exception:
        return {}, "unknown"


def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str    = os.environ.get("STORAGE_CONNECTION_STRING")
    mongo_uri   = os.environ.get("MONGODB_URI")
    storage_key = os.environ.get("STORAGE_KEY", "dWntrzHQ7hTveH+CstTTc13m+/QC9PkkPUPM7pdPcoTXUCC6jTU64s8r2rMuyDX9vnan2BFmj9Us+AStYFfaBg==")

    if not conn_str:
        return func.HttpResponse("Missing STORAGE_CONNECTION_STRING", status_code=500)
    if not mongo_uri:
        return func.HttpResponse("Missing MONGODB_URI", status_code=500)

    # Azure SWA identity
    user_id = req.headers.get("X-MS-CLIENT-PRINCIPAL-ID", "tester_user")
    claims, user_details = get_github_claims(req)

    # GitHub fields
    github_username = claims.get("urn:github:login", user_details)
    github_id       = claims.get("urn:github:id", "")
    user_email      = claims.get(
        "emailaddress",
        claims.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress", "")
    )

    try:
        clean_id   = "".join(filter(str.isalnum, user_id.lower()))
        share_name = f"fs-{clean_id[:10]}"

        service_client = ShareServiceClient.from_connection_string(conn_str)
        share_client   = service_client.get_share_client(share_name)

        # --- Share creation with proper error handling ---
        try:
            share_client.create_share(quota=5)
        except ResourceExistsError:
            # Share already exists — this is fine, user is re-provisioning
            pass
        except Exception as e:
            # Any other Azure error (conflict, lease, permissions etc.) — surface it
            return func.HttpResponse(
                f"ShareCreateError: {type(e).__name__}: {str(e)}",
                status_code=500
            )

        # Verify the share actually exists before telling the user it's ready
        try:
            props = share_client.get_share_properties()
        except Exception as e:
            return func.HttpResponse(
                f"Share verification failed — share may not exist: {str(e)}",
                status_code=500
            )

        # --- MongoDB update ---
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            db = client["file_shares_db"]
            db.shares.update_one(
                {"user_id": user_id},
                {"$set": {
                    "share_name":      share_name,
                    "github_username": github_username,
                    "github_id":       github_id,
                    "email":           user_email,
                }},
                upsert=True
            )
        except Exception as db_err:
            return func.HttpResponse(
                f"Share created but DB log failed: {str(db_err)}|{share_name}|{storage_key}",
                status_code=201
            )

        return func.HttpResponse(
            f"Success|{share_name}|{storage_key}",
            status_code=201
        )

    except Exception:
        return func.HttpResponse(traceback.format_exc(), status_code=500)