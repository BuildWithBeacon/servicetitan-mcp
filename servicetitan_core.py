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
BASE_URL = f"https://api.servicetitan.io/crm/v2/tenant/{TENANT_ID}"
CALLS_URL = f"https://api.servicetitan.io/telecom/v3/tenant/{TENANT_ID}/calls"

# FastMCP instance for Core ServiceTitan API
mcp = FastMCP("servicetitan-core")

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

# CUSTOMER ENDPOINTS

@mcp.tool()
async def get_customer_by_id(customer_id: str) -> dict:
    """Retrieve a customer from ServiceTitan by ID."""
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }
    url = f"{BASE_URL}/customers/{customer_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return { "error": f"Customer {customer_id} not found" }
        response.raise_for_status()
        return response.json()

# CALL ENDPOINTS

@mcp.tool()
async def summarize_calls(
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    agent_id: Optional[int] = None,
    caller_phone_number: Optional[str] = None,
    page_size: int = 10
) -> str:
    """Return a human-readable summary of recent calls."""
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    params = {
        "createdOnOrAfter": created_after,
        "createdBefore": created_before,
        "agentId": agent_id,
        "callerPhoneNumber": caller_phone_number,
        "page": 1,
        "pageSize": page_size
    }
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(CALLS_URL, headers=headers, params=clean_params)
        response.raise_for_status()
        data = response.json()

    calls = data.get("results") or []
    if not calls:
        return "No calls found for the specified filters."

    summaries = []
    for call in calls:
        agent = call.get("agent", {})
        summaries.append(
            f"• Call from {call.get('callerPhoneNumber', 'Unknown')} to {call.get('phoneNumberCalled', 'Unknown')}\n"
            f"  - Agent: {agent.get('name', 'Unknown')} ({'External' if agent.get('isExternal') else 'Internal'})\n"
            f"  - Duration: {call.get('duration', 0)}s\n"
            f"  - Created: {call.get('createdOn', 'N/A')}"
        )

    return "\n\n".join(summaries)

# APPOINTMENT ENDPOINTS

@mcp.tool()
async def get_appointments(
    ids: Optional[str] = None,
    job_id: Optional[int] = None,
    project_id: Optional[int] = None,
    number: Optional[str] = None,
    status: Optional[str] = None,
    starts_on_or_after: Optional[str] = None,
    starts_before: Optional[str] = None,
    technician_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    unused: Optional[bool] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 20,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Retrieve appointments from ServiceTitan with optional filters.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments"

    params = {
        "ids": ids,
        "jobId": job_id,
        "projectId": project_id,
        "number": number,
        "status": status,
        "startsOnOrAfter": starts_on_or_after,
        "startsBefore": starts_before,
        "technicianId": technician_id,
        "customerId": customer_id,
        "unused": unused,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 