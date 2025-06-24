from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List, Dict, Any

# Load .env values
load_dotenv()

# Env vars
CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")

# OAuth + API URLs
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
BASE_URL = f"https://api.servicetitan.io/forms/v2/tenant/{TENANT_ID}"

# FastMCP instance for Forms ServiceTitan API
mcp = FastMCP("servicetitan-forms")

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

# FORMS ENDPOINTS

@mcp.tool()
async def get_forms(
    has_conditional_logic: Optional[bool] = None,
    has_triggers: Optional[bool] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,  # Any, Published, Unpublished
    ids: Optional[str] = None,
    active: Optional[str] = None,  # True, Any, False
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Retrieve form data from ServiceTitan with optional filters.
    
    Args:
        has_conditional_logic: Filter by forms with conditional logic
        has_triggers: Filter by forms with triggers
        name: Filter by form name
        status: Form status (Any, Published, Unpublished)
        ids: Lookup by multiple IDs (comma separated)
        active: Filter by active status (True, Any, False)
        created_before: Return forms created before date/time (RFC3339 format)
        created_on_or_after: Return forms created on or after date/time (RFC3339 format)
        modified_before: Return forms modified before date/time (RFC3339 format)
        modified_on_or_after: Return forms modified on or after date/time (RFC3339 format)
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName for ascending, -FieldName for descending)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/forms"

    params = {
        "hasConditionalLogic": has_conditional_logic,
        "hasTriggers": has_triggers,
        "name": name,
        "status": status,
        "ids": ids,
        "active": active,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": "Forms not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_form_submissions(
    form_ids: Optional[str] = None,
    active: Optional[str] = None,  # True, Any, False
    created_by_id: Optional[int] = None,
    status: Optional[str] = None,  # Started, Completed, Any
    submitted_on_or_after: Optional[str] = None,
    submitted_before: Optional[str] = None,
    owner_type: Optional[str] = None,  # Job, Call, Customer, Location, Equipment, Technician, JobAppointment, Membership, Truck
    owners: Optional[List[Dict[str, Any]]] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Retrieve form submission data from ServiceTitan with optional filters.
    
    Args:
        form_ids: Form Ids (comma separated Ids)
        active: Filter by active status (True, Any, False)
        created_by_id: Creator user Id
        status: Submission status (Started, Completed, Any)
        submitted_on_or_after: Submission modified date on or after (RFC3339 format)
        submitted_before: Submission modified date before (RFC3339 format)
        owner_type: Type of owner (Job, Call, Customer, Location, Equipment, Technician, JobAppointment, Membership, Truck)
        owners: List of owner objects with type and id (e.g., [{"type": "Location", "id": 123}])
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (Available fields: Id, SubmittedOn, CreatedBy)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/submissions"

    params = {
        "formIds": form_ids,
        "active": active,
        "createdById": created_by_id,
        "status": status,
        "submittedOnOrAfter": submitted_on_or_after,
        "submittedBefore": submitted_before,
        "ownerType": owner_type,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Handle owners array parameter
    if owners:
        for i, owner in enumerate(owners):
            params[f"owners[{i}].type"] = owner.get("type")
            params[f"owners[{i}].id"] = owner.get("id")

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": "Form submissions not found"}
        response.raise_for_status()
        return response.json()

# JOB ATTACHMENT ENDPOINTS

@mcp.tool()
async def create_job_attachment(job_id: int, file_content: str) -> dict:
    """
    Create an attachment on the specified job.
    
    Args:
        job_id: Job ID to attach file to
        file_content: Base64 encoded file content or file content as string
    
    Returns:
        Dictionary with fileName of the created attachment
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/jobs/{job_id}/attachments"
    
    payload = {
        "file": file_content
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_attachments(
    job_id: int,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    sort: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Get attachments on the specified job.
    
    Args:
        job_id: Job ID to get attachments for
        created_before: Return attachments created before date/time (RFC3339 format)
        created_on_or_after: Return attachments created on or after date/time (RFC3339 format)
        sort: Sort by field
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
    
    Returns:
        Dictionary with job attachments data
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/jobs/{job_id}/attachments"

    params = {
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "sort": sort,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": f"Job {job_id} or attachments not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def download_job_attachment(attachment_id: int) -> dict:
    """
    Download a specified job attachment.
    
    Args:
        attachment_id: The ID of the job attachment to retrieve
    
    Returns:
        Dictionary with attachment content or error message
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/jobs/attachment/{attachment_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Attachment {attachment_id} not found"}
        response.raise_for_status()
        
        # For file downloads, we might want to return content info
        return {
            "attachment_id": attachment_id,
            "content_type": response.headers.get("content-type", "application/octet-stream"),
            "content_length": response.headers.get("content-length"),
            "content": response.content.decode("utf-8") if response.headers.get("content-type", "").startswith("text") else "Binary content (use appropriate client to download)",
            "status": "downloaded"
        }

if __name__ == "__main__":
    mcp.run(transport="stdio") 