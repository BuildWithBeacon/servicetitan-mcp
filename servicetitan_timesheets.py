from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("ServiceTitan Timesheets API")

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
def get_activities(page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None,
                  created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                  modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
                  active: Optional[str] = None, sort: Optional[str] = None) -> dict:
    """
    Get a list of timesheet activities with filtering options.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (RFC3339)
        created_on_or_after: Return items created on or after certain date/time (RFC3339)
        modified_before: Return items modified before certain date/time (RFC3339)
        modified_on_or_after: Return items modified on or after certain date/time (RFC3339)
        active: What kind of items should be returned (True, Any, False)
        sort: Applies sorting by specified fields
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/activities"
    
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if include_total is not None:
        params["includeTotal"] = include_total
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
    if sort is not None:
        params["sort"] = sort
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_activity(activity_id: int) -> dict:
    """
    Get a specific timesheet activity by ID.
    
    Args:
        activity_id: The ID of the activity to retrieve
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/activities/{activity_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def get_activity_categories(page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None,
                           created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                           modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
                           active: Optional[str] = None, sort: Optional[str] = None) -> dict:
    """
    Get a list of activity categories with filtering options.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (RFC3339)
        created_on_or_after: Return items created on or after certain date/time (RFC3339)
        modified_before: Return items modified before certain date/time (RFC3339)
        modified_on_or_after: Return items modified on or after certain date/time (RFC3339)
        active: What kind of items should be returned (True, Any, False)
        sort: Applies sorting by specified field (+FieldName for ascending, -FieldName for descending)
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/activity-categories"
    
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if include_total is not None:
        params["includeTotal"] = include_total
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
    if sort is not None:
        params["sort"] = sort
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_activity_category(category_id: int) -> dict:
    """
    Get a specific activity category by ID.
    
    Args:
        category_id: The ID of the activity category to retrieve
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/activity-categories/{category_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def get_activity_types(page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None,
                      created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                      modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
                      active: Optional[str] = None, sort: Optional[str] = None) -> dict:
    """
    Get a list of activity types with filtering options.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (RFC3339)
        created_on_or_after: Return items created on or after certain date/time (RFC3339)
        modified_before: Return items modified before certain date/time (RFC3339)
        modified_on_or_after: Return items modified on or after certain date/time (RFC3339)
        active: What kind of items should be returned (True, Any, False)
        sort: Applies sorting by specified field (+FieldName for ascending, -FieldName for descending)
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/activity-types"
    
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if include_total is not None:
        params["includeTotal"] = include_total
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
    if sort is not None:
        params["sort"] = sort
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_activity_type(activity_type_id: int) -> dict:
    """
    Get a specific activity type by ID.
    
    Args:
        activity_type_id: The ID of the activity type to retrieve
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/activity-types/{activity_type_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def export_activity_categories(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export activity categories feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/export/activity-categories"
    
    params = {}
    if from_token is not None:
        params["from"] = from_token
    if include_recent_changes is not None:
        params["includeRecentChanges"] = include_recent_changes
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def export_activity_types(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export activity types feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/export/activity-types"
    
    params = {}
    if from_token is not None:
        params["from"] = from_token
    if include_recent_changes is not None:
        params["includeRecentChanges"] = include_recent_changes
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def export_activities(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export activities feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/timesheets/v2/tenant/{TENANT_ID}/export/activities"
    
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