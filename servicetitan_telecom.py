from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("ServiceTitan Telecom API")

# ServiceTitan API configuration
BASE_URL = "https://api.servicetitan.io"
API_KEY = os.getenv("SERVICETITAN_API_KEY")
TENANT_ID = os.getenv("SERVICETITAN_TENANT_ID")
APP_KEY = os.getenv("SERVICETITAN_APP_KEY")

if not API_KEY or not TENANT_ID or not APP_KEY:
    raise ValueError("Missing required ServiceTitan environment variables: SERVICETITAN_API_KEY, SERVICETITAN_TENANT_ID, SERVICETITAN_APP_KEY")

# Common headers for API requests
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "ST-App-Key": APP_KEY,
    "Content-Type": "application/json"
}

@mcp.tool()
def get_calls_v3(page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None,
                ids: Optional[str] = None, created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
                active: Optional[str] = None, created_after: Optional[str] = None, modified_after: Optional[str] = None,
                campaign_id: Optional[int] = None, agent_id: Optional[int] = None, min_duration: Optional[int] = None,
                phone_number_called: Optional[str] = None, caller_phone_number: Optional[str] = None,
                agent_name: Optional[str] = None, agent_is_external: Optional[bool] = None,
                agent_external_id: Optional[int] = None, sort: Optional[str] = None) -> dict:
    """
    Get a feed of telecom calls with extensive filtering options (v3 API).
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        ids: Perform lookup by multiple IDs (maximum 50)
        created_before: Return items created before certain date/time (RFC3339)
        created_on_or_after: Return items created on or after certain date/time (RFC3339)
        modified_before: Return items modified before certain date/time (RFC3339)
        modified_on_or_after: Return items modified on or after certain date/time (RFC3339)
        active: What kind of items should be returned (True, Any, False)
        created_after: Return items created after certain date/time (RFC3339)
        modified_after: Return items modified after certain date/time (RFC3339)
        campaign_id: Campaign ID filter
        agent_id: Agent ID filter
        min_duration: Minimum call duration (number of seconds)
        phone_number_called: The phone number that was called
        caller_phone_number: The caller's phone number
        agent_name: Agent name filter
        agent_is_external: Is agent external flag
        agent_external_id: Agent external ID filter
        sort: Sorting field (Id, CreatedOn, ModifiedOn) with optional - prefix for descending
    """
    url = f"{BASE_URL}/telecom/v3/tenant/{TENANT_ID}/calls"
    
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if include_total is not None:
        params["includeTotal"] = include_total
    if ids is not None:
        params["ids"] = ids
    if created_before is not None:
        params["createdBefore"] = created_before
    if created_on_or_after is not None:
        params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None:
        params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None:
        params["modifiedOnOrAfter"] = modified_on_or_after
    if active is not None:
        params["active"] = active
    if created_after is not None:
        params["createdAfter"] = created_after
    if modified_after is not None:
        params["modifiedAfter"] = modified_after
    if campaign_id is not None:
        params["campaignId"] = campaign_id
    if agent_id is not None:
        params["agentId"] = agent_id
    if min_duration is not None:
        params["minDuration"] = min_duration
    if phone_number_called is not None:
        params["phoneNumberCalled"] = phone_number_called
    if caller_phone_number is not None:
        params["callerPhoneNumber"] = caller_phone_number
    if agent_name is not None:
        params["agentName"] = agent_name
    if agent_is_external is not None:
        params["agentIsExternal"] = agent_is_external
    if agent_external_id is not None:
        params["agentExternalId"] = agent_external_id
    if sort is not None:
        params["sort"] = sort
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_opt_outs() -> dict:
    """
    Get all opt-outs for the tenant. Numbers are returned in E.164 format.
    """
    url = f"{BASE_URL}/telecom/v3/tenant/{TENANT_ID}/optinouts/optouts"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def add_opt_outs(opt_out_data: dict) -> dict:
    """
    Add opt-outs for specified phone numbers.
    
    Args:
        opt_out_data: Data containing optOutType and contactNumbers array
    """
    url = f"{BASE_URL}/telecom/v3/tenant/{TENANT_ID}/optinouts/optouts"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=opt_out_data)
        return response.json()

@mcp.tool()
def get_opt_out_status(phone_numbers_data: dict) -> dict:
    """
    Get opt-out status for specific phone numbers.
    
    Args:
        phone_numbers_data: Data containing contactNumbers array to check
    """
    url = f"{BASE_URL}/telecom/v3/tenant/{TENANT_ID}/optinouts/optouts/getlist"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=phone_numbers_data)
        return response.json()

@mcp.tool()
def get_call_details(call_id: int) -> dict:
    """
    Get detailed information for a specific call (v2 API).
    
    Args:
        call_id: The ID of the call to retrieve
    """
    url = f"{BASE_URL}/telecom/v2/tenant/{TENANT_ID}/calls/{call_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def update_call(call_id: int, call_data: dict) -> dict:
    """
    Update an existing call (v2 API).
    
    Args:
        call_id: The ID of the call to update
        call_data: Call data containing fields to update (callType, excuseMemo, campaignId, jobId, agentId, reason, customer, location)
    """
    url = f"{BASE_URL}/telecom/v2/tenant/{TENANT_ID}/calls/{call_id}"
    
    with httpx.Client() as client:
        response = client.put(url, headers=HEADERS, json=call_data)
        return response.json()

@mcp.tool()
def get_calls_v2(modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
                created_on_or_after: Optional[str] = None, modified_after: Optional[str] = None,
                min_duration: Optional[int] = None, phone_number_called: Optional[str] = None,
                campaign_id: Optional[int] = None, agent_id: Optional[int] = None, agent_name: Optional[str] = None,
                agent_is_external: Optional[bool] = None, agent_external_id: Optional[int] = None,
                order_by: Optional[str] = None, order_by_direction: Optional[str] = None,
                active_only: Optional[bool] = None, created_after: Optional[str] = None,
                created_before: Optional[str] = None, ids: Optional[List[int]] = None,
                page: Optional[int] = None, page_size: Optional[int] = None) -> dict:
    """
    Get filtered calls with legacy v2 API format.
    
    Args:
        modified_before: Modified before certain date/time (RFC3339), not inclusive
        modified_on_or_after: Modified on or after certain date/time (RFC3339), inclusive
        created_on_or_after: Created on or after certain date/time (RFC3339), inclusive
        modified_after: Modified after certain date/time (RFC3339), not inclusive
        min_duration: Minimum call duration
        phone_number_called: The phone number that was called
        campaign_id: Campaign ID filter
        agent_id: Agent ID filter
        agent_name: Agent name filter
        agent_is_external: Is agent external flag
        agent_external_id: Agent external ID filter
        order_by: Sorting field ("Id", "createdOn", "modifiedOn")
        order_by_direction: Sorting direction ("asc" or "desc")
        active_only: Active calls only filter
        created_after: Created after certain date/time (RFC3339)
        created_before: Created before certain date/time (RFC3339)
        ids: Array of call IDs to filter
        page: Page number
        page_size: Page size
    """
    url = f"{BASE_URL}/telecom/v2/tenant/{TENANT_ID}/calls"
    
    params = {}
    if modified_before is not None:
        params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None:
        params["modifiedOnOrAfter"] = modified_on_or_after
    if created_on_or_after is not None:
        params["createdOnOrAfter"] = created_on_or_after
    if modified_after is not None:
        params["modifiedAfter"] = modified_after
    if min_duration is not None:
        params["minDuration"] = min_duration
    if phone_number_called is not None:
        params["phoneNumberCalled"] = phone_number_called
    if campaign_id is not None:
        params["campaignId"] = campaign_id
    if agent_id is not None:
        params["agentId"] = agent_id
    if agent_name is not None:
        params["agentName"] = agent_name
    if agent_is_external is not None:
        params["agentIsExternal"] = agent_is_external
    if agent_external_id is not None:
        params["agentExternalId"] = agent_external_id
    if order_by is not None:
        params["orderBy"] = order_by
    if order_by_direction is not None:
        params["orderByDirection"] = order_by_direction
    if active_only is not None:
        params["activeOnly"] = active_only
    if created_after is not None:
        params["createdAfter"] = created_after
    if created_before is not None:
        params["createdBefore"] = created_before
    if ids is not None:
        params["ids"] = ids
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_call_recording(call_id: int) -> bytes:
    """
    Get the audio recording of a call as binary data.
    
    Args:
        call_id: The ID of the call to get recording for
    """
    url = f"{BASE_URL}/telecom/v2/tenant/{TENANT_ID}/calls/{call_id}/recording"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.content

@mcp.tool()
def get_call_voicemail(call_id: int) -> bytes:
    """
    Get the voicemail of a call as binary data.
    
    Args:
        call_id: The ID of the call to get voicemail for
    """
    url = f"{BASE_URL}/telecom/v2/tenant/{TENANT_ID}/calls/{call_id}/voicemail"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.content

@mcp.tool()
def export_calls(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export telecom calls feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/telecom/v2/tenant/{TENANT_ID}/export/calls"
    
    params = {}
    if from_token is not None:
        params["from"] = from_token
    if include_recent_changes is not None:
        params["includeRecentChanges"] = include_recent_changes
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 