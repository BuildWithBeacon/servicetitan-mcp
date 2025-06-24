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

# FastMCP instance for JPM v2 API
mcp = FastMCP("servicetitan-jpm")

async def get_access_token() -> str:
    """Fetch OAuth2 access token from ServiceTitan."""
    if not CLIENT_ID or not CLIENT_SECRET or not APP_KEY or not TENANT_ID:
        error_msg = "ERROR_ENV: One or more ServiceTitan environment variables are not set."
        raise ValueError(error_msg)

    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
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

# =============================================================================
# APPOINTMENTS ENDPOINTS
# =============================================================================

@mcp.tool()
async def get_appointment_by_id(appointment_id: str) -> dict:
    """
    Get appointment specified by ID.
    
    Args:
        appointment_id: The ID of the appointment to retrieve (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments/{appointment_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Appointment {appointment_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_appointment(appointment_id: str) -> dict:
    """
    Delete appointment with specified ID.
    
    Args:
        appointment_id: The ID of the appointment to delete (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments/{appointment_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Appointment {appointment_id} not found"}
        if response.status_code == 409:
            return {"error": f"Appointment {appointment_id} is in a state that doesn't allow deletion"}
        response.raise_for_status()
        return {"success": f"Appointment {appointment_id} deleted successfully"}

@mcp.tool()
async def create_appointment(
    job_id: int,
    start: str,
    end: str,
    arrival_window_start: Optional[str] = None,
    arrival_window_end: Optional[str] = None,
    special_instructions: Optional[str] = None
) -> dict:
    """
    Create a new appointment.
    
    Args:
        job_id: ID of the job (required)
        start: Start date/time in RFC3339 format (required)
        end: End date/time in RFC3339 format (required)
        arrival_window_start: Arrival window start time in RFC3339 format
        arrival_window_end: Arrival window end time in RFC3339 format
        special_instructions: Special instructions for the appointment
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments"

    request_body = {
        "jobId": job_id,
        "start": start,
        "end": end
    }

    if arrival_window_start is not None:
        request_body["arrivalWindowStart"] = arrival_window_start
    if arrival_window_end is not None:
        request_body["arrivalWindowEnd"] = arrival_window_end
    if special_instructions is not None:
        request_body["specialInstructions"] = special_instructions

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def reschedule_appointment(
    appointment_id: str,
    start: str,
    end: str,
    arrival_window_start: Optional[str] = None,
    arrival_window_end: Optional[str] = None
) -> dict:
    """
    Reschedule an existing appointment.
    
    Args:
        appointment_id: ID of the appointment to reschedule (required)
        start: New start date/time in RFC3339 format (required)
        end: New end date/time in RFC3339 format (required)
        arrival_window_start: New arrival window start time in RFC3339 format
        arrival_window_end: New arrival window end time in RFC3339 format
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments/{appointment_id}/reschedule"

    request_body = {
        "start": start,
        "end": end
    }

    if arrival_window_start is not None:
        request_body["arrivalWindowStart"] = arrival_window_start
    if arrival_window_end is not None:
        request_body["arrivalWindowEnd"] = arrival_window_end

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Appointment {appointment_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def hold_appointment(
    appointment_id: str,
    reason: str
) -> dict:
    """
    Put an appointment on hold.
    
    Args:
        appointment_id: ID of the appointment to hold (required)
        reason: Reason for holding the appointment (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments/{appointment_id}/hold"

    request_body = {"reason": reason}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Appointment {appointment_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def remove_appointment_hold(appointment_id: str) -> dict:
    """
    Remove hold from an appointment.
    
    Args:
        appointment_id: ID of the appointment to remove hold from (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments/{appointment_id}/hold"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Appointment {appointment_id} not found"}
        response.raise_for_status()
        return {"success": f"Hold removed from appointment {appointment_id}"}

@mcp.tool()
async def update_appointment_special_instructions(
    appointment_id: str,
    special_instructions: str
) -> dict:
    """
    Update special instructions for an appointment.
    
    Args:
        appointment_id: ID of the appointment (required)
        special_instructions: Special instructions text (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments/{appointment_id}/special-instructions"

    request_body = {"specialInstructions": special_instructions}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Appointment {appointment_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def confirm_appointment(appointment_id: str) -> dict:
    """
    Confirm an appointment.
    
    Args:
        appointment_id: ID of the appointment to confirm (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments/{appointment_id}/confirmation"

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json={})
        if response.status_code == 404:
            return {"error": f"Appointment {appointment_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def remove_appointment_confirmation(appointment_id: str) -> dict:
    """
    Remove confirmation from an appointment.
    
    Args:
        appointment_id: ID of the appointment to remove confirmation from (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/appointments/{appointment_id}/confirmation"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Appointment {appointment_id} not found"}
        response.raise_for_status()
        return {"success": f"Confirmation removed from appointment {appointment_id}"}

# =============================================================================
# JOBS ENDPOINTS
# =============================================================================

@mcp.tool()
async def get_job_by_id(
    job_id: str,
    include_custom_fields: Optional[bool] = None
) -> dict:
    """
    Get job specified by ID.
    
    Args:
        job_id: The ID of the job to retrieve (required)
        include_custom_fields: Whether to include custom fields in response
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}"

    params = {}
    if include_custom_fields is not None:
        params["includeCustomFields"] = include_custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_job(
    job_id: str,
    summary: Optional[str] = None,
    customer_id: Optional[int] = None,
    location_id: Optional[int] = None,
    job_type_id: Optional[int] = None,
    priority: Optional[str] = None,
    campaign_id: Optional[int] = None,
    business_unit_id: Optional[int] = None,
    custom_fields: Optional[list] = None
) -> dict:
    """
    Update an existing job.
    
    Args:
        job_id: ID of the job to update (required)
        summary: Job summary
        customer_id: Customer ID
        location_id: Location ID
        job_type_id: Job type ID
        priority: Job priority
        campaign_id: Campaign ID
        business_unit_id: Business unit ID
        custom_fields: List of custom fields
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}"

    request_body = {}

    if summary is not None:
        request_body["summary"] = summary
    if customer_id is not None:
        request_body["customerId"] = customer_id
    if location_id is not None:
        request_body["locationId"] = location_id
    if job_type_id is not None:
        request_body["jobTypeId"] = job_type_id
    if priority is not None:
        request_body["priority"] = priority
    if campaign_id is not None:
        request_body["campaignId"] = campaign_id
    if business_unit_id is not None:
        request_body["businessUnitId"] = business_unit_id
    if custom_fields is not None:
        request_body["customFields"] = custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_jobs(
    ids: Optional[str] = None,
    number: Optional[str] = None,
    project_id: Optional[int] = None,
    job_type_ids: Optional[str] = None,
    customer_id: Optional[int] = None,
    location_id: Optional[int] = None,
    business_unit_ids: Optional[str] = None,
    campaign_ids: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    completed_on_or_after: Optional[str] = None,
    completed_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of jobs with optional filters.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        number: Job number filter
        project_id: Project ID filter
        job_type_ids: Job type IDs filter (comma-separated)
        customer_id: Customer ID filter
        location_id: Location ID filter
        business_unit_ids: Business unit IDs filter (comma-separated)
        campaign_ids: Campaign IDs filter (comma-separated)
        priority: Priority filter
        status: Status filter
        created_on_or_after: Created on or after date (RFC3339)
        created_before: Created before date (RFC3339)
        modified_on_or_after: Modified on or after date (RFC3339)
        modified_before: Modified before date (RFC3339)
        completed_on_or_after: Completed on or after date (RFC3339)
        completed_before: Completed before date (RFC3339)
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName ascending, -FieldName descending)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs"

    params = {
        "ids": ids,
        "number": number,
        "projectId": project_id,
        "jobTypeIds": job_type_ids,
        "customerId": customer_id,
        "locationId": location_id,
        "businessUnitIds": business_unit_ids,
        "campaignIds": campaign_ids,
        "priority": priority,
        "status": status,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "completedOnOrAfter": completed_on_or_after,
        "completedBefore": completed_before,
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

@mcp.tool()
async def create_job(
    job_type_id: int,
    customer_id: int,
    location_id: int,
    business_unit_id: int,
    summary: Optional[str] = None,
    priority: Optional[str] = None,
    campaign_id: Optional[int] = None,
    custom_fields: Optional[list] = None
) -> dict:
    """
    Create a new job.
    
    Args:
        job_type_id: Job type ID (required)
        customer_id: Customer ID (required)
        location_id: Location ID (required)
        business_unit_id: Business unit ID (required)
        summary: Job summary
        priority: Job priority
        campaign_id: Campaign ID
        custom_fields: List of custom fields
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs"

    request_body = {
        "jobTypeId": job_type_id,
        "customerId": customer_id,
        "locationId": location_id,
        "businessUnitId": business_unit_id
    }

    if summary is not None:
        request_body["summary"] = summary
    if priority is not None:
        request_body["priority"] = priority
    if campaign_id is not None:
        request_body["campaignId"] = campaign_id
    if custom_fields is not None:
        request_body["customFields"] = custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def cancel_job(
    job_id: str,
    reason_id: int
) -> dict:
    """
    Cancel a job.
    
    Args:
        job_id: ID of the job to cancel (required)
        reason_id: Reason ID for cancellation (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}/cancel"

    request_body = {"reasonId": reason_id}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def remove_job_cancellation(job_id: str) -> dict:
    """
    Remove cancellation from a job.
    
    Args:
        job_id: ID of the job to remove cancellation from (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}/remove-cancellation"

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json={})
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return {"success": f"Cancellation removed from job {job_id}"}

@mcp.tool()
async def hold_job(
    job_id: str,
    reason_id: int
) -> dict:
    """
    Put a job on hold.
    
    Args:
        job_id: ID of the job to hold (required)
        reason_id: Reason ID for holding the job (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}/hold"

    request_body = {"reasonId": reason_id}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def complete_job(
    job_id: str,
    completed_on: Optional[str] = None
) -> dict:
    """
    Mark a job as complete.
    
    Args:
        job_id: ID of the job to complete (required)
        completed_on: Completion date/time in RFC3339 format
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}/complete"

    request_body = {}
    if completed_on is not None:
        request_body["completedOn"] = completed_on

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_notes(
    job_id: str,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Get notes for a specific job.
    
    Args:
        job_id: ID of the job (required)
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}/notes"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def add_job_note(
    job_id: str,
    text: str,
    is_important: Optional[bool] = False
) -> dict:
    """
    Add a note to a job.
    
    Args:
        job_id: ID of the job (required)
        text: Note text (required)
        is_important: Whether the note is important
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}/notes"

    request_body = {"text": text}
    if is_important is not None:
        request_body["isImportant"] = is_important

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_history(
    job_id: str,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Get history for a specific job.
    
    Args:
        job_id: ID of the job (required)
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}/history"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_messages(
    job_id: str,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Get messages for a specific job.
    
    Args:
        job_id: ID of the job (required)
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/jobs/{job_id}/messages"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return response.json()

# =============================================================================
# JOB TYPES AND CONFIGURATION ENDPOINTS
# =============================================================================

@mcp.tool()
async def get_job_cancel_reasons() -> dict:
    """
    Get available job cancellation reasons.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/job-cancel-reasons"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_hold_reasons() -> dict:
    """
    Get available job hold reasons.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/job-hold-reasons"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_types(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    active: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """
    Get job types.
    
    Args:
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        active: Filter by active status ("True", "Any", "False")
        sort: Sort by field (+FieldName ascending, -FieldName descending)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/job-types"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "active": active,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_job_type(
    name: str,
    summary: Optional[str] = None,
    active: Optional[bool] = True
) -> dict:
    """
    Create a new job type.
    
    Args:
        name: Name of the job type (required)
        summary: Summary/description of the job type
        active: Whether the job type is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/job-types"

    request_body = {"name": name}

    if summary is not None:
        request_body["summary"] = summary
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_type_by_id(job_type_id: str) -> dict:
    """
    Get a specific job type by ID.
    
    Args:
        job_type_id: ID of the job type (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/job-types/{job_type_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Job type {job_type_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_job_type(
    job_type_id: str,
    name: Optional[str] = None,
    summary: Optional[str] = None,
    active: Optional[bool] = None
) -> dict:
    """
    Update an existing job type.
    
    Args:
        job_type_id: ID of the job type to update (required)
        name: Name of the job type
        summary: Summary/description of the job type
        active: Whether the job type is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/job-types/{job_type_id}"

    request_body = {}

    if name is not None:
        request_body["name"] = name
    if summary is not None:
        request_body["summary"] = summary
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Job type {job_type_id} not found"}
        response.raise_for_status()
        return response.json()

# =============================================================================
# PROJECTS ENDPOINTS
# =============================================================================

@mcp.tool()
async def get_project_by_id(
    project_id: str,
    include_custom_fields: Optional[bool] = None
) -> dict:
    """
    Get project specified by ID.
    
    Args:
        project_id: The ID of the project to retrieve (required)
        include_custom_fields: Whether to include custom fields in response
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/projects/{project_id}"

    params = {}
    if include_custom_fields is not None:
        params["includeCustomFields"] = include_custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return {"error": f"Project {project_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_project(
    project_id: str,
    name: Optional[str] = None,
    summary: Optional[str] = None,
    status_id: Optional[int] = None,
    substatus_id: Optional[int] = None,
    custom_fields: Optional[list] = None
) -> dict:
    """
    Update an existing project.
    
    Args:
        project_id: ID of the project to update (required)
        name: Project name
        summary: Project summary
        status_id: Status ID
        substatus_id: Substatus ID
        custom_fields: List of custom fields
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/projects/{project_id}"

    request_body = {}

    if name is not None:
        request_body["name"] = name
    if summary is not None:
        request_body["summary"] = summary
    if status_id is not None:
        request_body["statusId"] = status_id
    if substatus_id is not None:
        request_body["substatusId"] = substatus_id
    if custom_fields is not None:
        request_body["customFields"] = custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Project {project_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_projects(
    ids: Optional[str] = None,
    number: Optional[str] = None,
    name: Optional[str] = None,
    customer_id: Optional[int] = None,
    location_id: Optional[int] = None,
    business_unit_ids: Optional[str] = None,
    project_manager_ids: Optional[str] = None,
    status_ids: Optional[str] = None,
    substatus_ids: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of projects with optional filters.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        number: Project number filter
        name: Project name filter
        customer_id: Customer ID filter
        location_id: Location ID filter
        business_unit_ids: Business unit IDs filter (comma-separated)
        project_manager_ids: Project manager IDs filter (comma-separated)
        status_ids: Status IDs filter (comma-separated)
        substatus_ids: Substatus IDs filter (comma-separated)
        created_on_or_after: Created on or after date (RFC3339)
        created_before: Created before date (RFC3339)
        modified_on_or_after: Modified on or after date (RFC3339)
        modified_before: Modified before date (RFC3339)
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName ascending, -FieldName descending)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/projects"

    params = {
        "ids": ids,
        "number": number,
        "name": name,
        "customerId": customer_id,
        "locationId": location_id,
        "businessUnitIds": business_unit_ids,
        "projectManagerIds": project_manager_ids,
        "statusIds": status_ids,
        "substatusIds": substatus_ids,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
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

@mcp.tool()
async def create_project(
    name: str,
    customer_id: int,
    location_id: int,
    business_unit_id: int,
    project_manager_id: int,
    summary: Optional[str] = None,
    status_id: Optional[int] = None,
    substatus_id: Optional[int] = None,
    custom_fields: Optional[list] = None
) -> dict:
    """
    Create a new project.
    
    Args:
        name: Project name (required)
        customer_id: Customer ID (required)
        location_id: Location ID (required)
        business_unit_id: Business unit ID (required)
        project_manager_id: Project manager ID (required)
        summary: Project summary
        status_id: Status ID
        substatus_id: Substatus ID
        custom_fields: List of custom fields
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/projects"

    request_body = {
        "name": name,
        "customerId": customer_id,
        "locationId": location_id,
        "businessUnitId": business_unit_id,
        "projectManagerId": project_manager_id
    }

    if summary is not None:
        request_body["summary"] = summary
    if status_id is not None:
        request_body["statusId"] = status_id
    if substatus_id is not None:
        request_body["substatusId"] = substatus_id
    if custom_fields is not None:
        request_body["customFields"] = custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def attach_job_to_project(
    project_id: str,
    job_id: str
) -> dict:
    """
    Attach a job to a project.
    
    Args:
        project_id: ID of the project (required)
        job_id: ID of the job to attach (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/projects/{project_id}/attach-job/{job_id}"

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json={})
        if response.status_code == 404:
            return {"error": f"Project {project_id} or job {job_id} not found"}
        response.raise_for_status()
        return {"success": f"Job {job_id} attached to project {project_id}"}

@mcp.tool()
async def detach_job_from_project(job_id: str) -> dict:
    """
    Detach a job from its project.
    
    Args:
        job_id: ID of the job to detach (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/projects/detach-job/{job_id}"

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json={})
        if response.status_code == 404:
            return {"error": f"Job {job_id} not found"}
        response.raise_for_status()
        return {"success": f"Job {job_id} detached from project"}

# =============================================================================
# EXPORT ENDPOINTS
# =============================================================================

@mcp.tool()
async def export_jobs() -> dict:
    """
    Export jobs data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/export/jobs"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_projects() -> dict:
    """
    Export projects data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/export/projects"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_appointments() -> dict:
    """
    Export appointments data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/export/appointments"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_job_notes() -> dict:
    """
    Export job notes data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/export/job-notes"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_project_notes() -> dict:
    """
    Export project notes data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/export/project-notes"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_job_history() -> dict:
    """
    Export job history data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/jpm/v2/tenant/{TENANT_ID}/export/job-history"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 