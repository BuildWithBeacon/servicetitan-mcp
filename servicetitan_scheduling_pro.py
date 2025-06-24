from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("ServiceTitan Scheduling Pro API")

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
def get_router_sessions(router_id: str, created_before: Optional[str] = None, 
                       created_on_or_after: Optional[str] = None, modified_before: Optional[str] = None,
                       modified_on_or_after: Optional[str] = None, page: Optional[int] = None,
                       page_size: Optional[int] = None, include_total: Optional[bool] = None) -> dict:
    """
    Get a paginated list of sessions for a specific router.
    
    Args:
        router_id: The ID of the router
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
    """
    url = f"{BASE_URL}/schedulingpro/v2/tenant/{TENANT_ID}/routers/{router_id}/sessions"
    
    params = {}
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
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_router_performance(router_id: str, session_created_on_or_after: str, session_created_before: str) -> dict:
    """
    Get performance data for a specific router.
    
    Args:
        router_id: The ID of the router
        session_created_on_or_after: Filter sessions created on or after this date/time (required)
        session_created_before: Filter sessions created before this date/time (required)
    """
    url = f"{BASE_URL}/schedulingpro/v2/tenant/{TENANT_ID}/routers/{router_id}/performance"
    
    params = {
        "sessionCreatedOnOrAfter": session_created_on_or_after,
        "sessionCreatedBefore": session_created_before
    }
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_schedulers(created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                  modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
                  page: Optional[int] = None, page_size: Optional[int] = None, 
                  include_total: Optional[bool] = None) -> dict:
    """
    Get a list of schedulers with optional filtering.
    
    Args:
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
    """
    url = f"{BASE_URL}/schedulingpro/v2/tenant/{TENANT_ID}/schedulers"
    
    params = {}
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
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_scheduler_sessions(scheduler_id: str, created_before: Optional[str] = None,
                          created_on_or_after: Optional[str] = None, modified_before: Optional[str] = None,
                          modified_on_or_after: Optional[str] = None, page: Optional[int] = None,
                          page_size: Optional[int] = None, include_total: Optional[bool] = None) -> dict:
    """
    Get a paginated list of sessions for a specific scheduler.
    
    Args:
        scheduler_id: The ID of the scheduler
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
    """
    url = f"{BASE_URL}/schedulingpro/v2/tenant/{TENANT_ID}/schedulers/{scheduler_id}/sessions"
    
    params = {}
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
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_scheduler_performance(scheduler_id: str, session_created_on_or_after: str, session_created_before: str) -> dict:
    """
    Get performance data for a specific scheduler.
    
    Args:
        scheduler_id: The ID of the scheduler
        session_created_on_or_after: Filter sessions created on or after this date/time (required)
        session_created_before: Filter sessions created before this date/time (required)
    """
    url = f"{BASE_URL}/schedulingpro/v2/tenant/{TENANT_ID}/schedulers/{scheduler_id}/performance"
    
    params = {
        "sessionCreatedOnOrAfter": session_created_on_or_after,
        "sessionCreatedBefore": session_created_before
    }
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 