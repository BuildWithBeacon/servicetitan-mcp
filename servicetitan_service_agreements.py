from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("ServiceTitan Service Agreements API")

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
def export_service_agreements(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export service agreements feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/service-agreements/v2/tenant/{TENANT_ID}/export/service-agreements"
    
    params = {}
    if from_token is not None:
        params["from"] = from_token
    if include_recent_changes is not None:
        params["includeRecentChanges"] = include_recent_changes
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_service_agreements(ids: Optional[str] = None, customer_ids: Optional[str] = None, 
                          business_unit_ids: Optional[str] = None, status: Optional[str] = None,
                          created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                          modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
                          page: Optional[int] = None, page_size: Optional[int] = None,
                          include_total: Optional[bool] = None, sort: Optional[str] = None) -> dict:
    """
    Get a list of service agreements with optional filtering.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        customer_ids: Filters by customer IDs
        business_unit_ids: Filters by business unit IDs
        status: Filters by service agreement status (Draft, Sent, Rejected, Accepted, Activated, Canceled, Expired, AutoRenew)
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Applies sorting by the specified field (+FieldName for ascending, -FieldName for descending)
    """
    url = f"{BASE_URL}/service-agreements/v2/tenant/{TENANT_ID}/service-agreements"
    
    params = {}
    if ids is not None:
        params["ids"] = ids
    if customer_ids is not None:
        params["customerIds"] = customer_ids
    if business_unit_ids is not None:
        params["businessUnitIds"] = business_unit_ids
    if status is not None:
        params["status"] = status
    if created_before is not None:
        params["createdBefore"] = created_before
    if created_on_or_after is not None:
        params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None:
        params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None:
        params["modifiedOnOrAfter"] = modified_on_or_after
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if include_total is not None:
        params["includeTotal"] = include_total
    if sort is not None:
        params["sort"] = sort
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_service_agreement(agreement_id: int) -> dict:
    """
    Get a specific service agreement by ID.
    
    Args:
        agreement_id: The ID of the service agreement to retrieve
    """
    url = f"{BASE_URL}/service-agreements/v2/tenant/{TENANT_ID}/service-agreements/{agreement_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 