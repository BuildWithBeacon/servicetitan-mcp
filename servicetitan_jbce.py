from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional

# Load .env values
load_dotenv()

# Env vars
CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")

# OAuth + API URLs
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
BASE_URL = f"https://api.servicetitan.io/jbce/v2/tenant/{TENANT_ID}"

# FastMCP instance for JBCE ServiceTitan API
mcp = FastMCP("servicetitan-jbce")

async def get_access_token() -> str:
    """Fetch OAuth2 access token from ServiceTitan."""
    if not CLIENT_ID or not CLIENT_SECRET or not APP_KEY or not TENANT_ID:
        error_msg = "ERROR_ENV: One or more ServiceTitan environment variables are not set."
        raise ValueError(error_msg)

    async with httpx.AsyncClient() as client:
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        response = await client.post(TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()
        token_response_json = response.json()
        
        access_token = token_response_json.get("access_token")
        
        if not isinstance(access_token, str):
            error_msg = f"ERROR_TOKEN: access_token is not a string or is missing. Type: {type(access_token)}, Value: {access_token}"
            raise TypeError(error_msg)
            
        return access_token

# CALL REASONS ENDPOINTS

@mcp.tool()
async def get_call_reasons(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    active: Optional[str] = None,  # True, Any, False
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """
    Gets a list of call reasons from ServiceTitan JBCE API.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        active: What kind of items should be returned (True, Any, False) - only active items by default
        created_before: Return items created before certain date/time (RFC3339 format)
        created_on_or_after: Return items created on or after certain date/time (RFC3339 format)
        modified_before: Return items modified before certain date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after certain date/time (RFC3339 format)
        sort: Applies sorting by field (+FieldName ascending, -FieldName descending). 
              Available fields: Id, ModifiedOn, CreatedOn
    
    Returns:
        dict: JSON response containing call reasons data with fields:
              - id: Call reason ID
              - name: Call reason name
              - isLead: Whether this is a lead call reason
              - active: Whether the call reason is active
              - createdOn: Creation timestamp
              - modifiedOn: Last modification timestamp
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/call-reasons"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "active": active,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": "Call reasons not found"}
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 