from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("ServiceTitan Sales & Estimates API")

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
def get_estimate(estimate_id: int) -> dict:
    """
    Get a specific estimate by ID.
    
    Args:
        estimate_id: The ID of the estimate to retrieve
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/{estimate_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def update_estimate(estimate_id: int, estimate_data: dict) -> dict:
    """
    Update an existing estimate.
    
    Args:
        estimate_id: The ID of the estimate to update
        estimate_data: The estimate data containing name, summary, tax, status, items, etc.
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/{estimate_id}"
    
    with httpx.Client() as client:
        response = client.put(url, headers=HEADERS, json=estimate_data)
        return response.json()

@mcp.tool()
def get_estimates(job_id: Optional[int] = None, project_id: Optional[int] = None, job_number: Optional[str] = None, 
                 total_greater: Optional[float] = None, total_less: Optional[float] = None, sold_by_id: Optional[int] = None,
                 sold_by_employee_id: Optional[int] = None, ids: Optional[str] = None, page: Optional[int] = None,
                 page_size: Optional[int] = None, include_total: Optional[bool] = None, sold_after: Optional[str] = None,
                 sold_before: Optional[str] = None, status: Optional[str] = None, active: Optional[str] = None,
                 order_by: Optional[str] = None, order_by_direction: Optional[str] = None, created_before: Optional[str] = None,
                 created_on_or_after: Optional[str] = None, modified_before: Optional[str] = None,
                 modified_on_or_after: Optional[str] = None, location_id: Optional[int] = None) -> dict:
    """
    Get a list of estimates with optional filtering.
    
    Args:
        job_id: Filter by job ID
        project_id: Filter by project ID
        job_number: Filter by job number
        total_greater: Filter by estimates with total greater than this amount
        total_less: Filter by estimates with total less than this amount
        sold_by_id: Filter by who sold the estimate
        sold_by_employee_id: Filter by employee ID who sold the estimate
        ids: Perform lookup by multiple IDs (maximum 50)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        sold_after: Filter by estimates sold after this date
        sold_before: Filter by estimates sold before this date
        status: Filter by estimate status
        active: What kind of items should be returned (True, Any, False)
        order_by: Field to order by
        order_by_direction: Order direction (asc/desc)
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        location_id: Filter by location ID
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates"
    
    params = {}
    if job_id is not None:
        params["jobId"] = job_id
    if project_id is not None:
        params["projectId"] = project_id
    if job_number is not None:
        params["jobNumber"] = job_number
    if total_greater is not None:
        params["totalGreater"] = total_greater
    if total_less is not None:
        params["totalLess"] = total_less
    if sold_by_id is not None:
        params["soldById"] = sold_by_id
    if sold_by_employee_id is not None:
        params["soldByEmployeeId"] = sold_by_employee_id
    if ids is not None:
        params["ids"] = ids
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if include_total is not None:
        params["includeTotal"] = include_total
    if sold_after is not None:
        params["soldAfter"] = sold_after
    if sold_before is not None:
        params["soldBefore"] = sold_before
    if status is not None:
        params["status"] = status
    if active is not None:
        params["active"] = active
    if order_by is not None:
        params["orderBy"] = order_by
    if order_by_direction is not None:
        params["orderByDirection"] = order_by_direction
    if created_before is not None:
        params["createdBefore"] = created_before
    if created_on_or_after is not None:
        params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None:
        params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None:
        params["modifiedOnOrAfter"] = modified_on_or_after
    if location_id is not None:
        params["locationId"] = location_id
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def create_estimate(estimate_data: dict) -> dict:
    """
    Create a new estimate.
    
    Args:
        estimate_data: The estimate data containing name, summary, jobId, projectId, locationId, items, etc.
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=estimate_data)
        return response.json()

@mcp.tool()
def get_estimate_items(estimate_id: Optional[int] = None, ids: Optional[str] = None, active: Optional[str] = None,
                      created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                      page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None) -> dict:
    """
    Get estimate items with optional filtering.
    
    Args:
        estimate_id: Filter by estimate ID
        ids: Perform lookup by multiple IDs (maximum 50)
        active: What kind of items should be returned (True, Any, False)
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/items"
    
    params = {}
    if estimate_id is not None:
        params["estimateId"] = estimate_id
    if ids is not None:
        params["ids"] = ids
    if active is not None:
        params["active"] = active
    if created_before is not None:
        params["createdBefore"] = created_before
    if created_on_or_after is not None:
        params["createdOnOrAfter"] = created_on_or_after
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
def sell_estimate(estimate_id: int, sold_by: int) -> dict:
    """
    Mark an estimate as sold.
    
    Args:
        estimate_id: The ID of the estimate to sell
        sold_by: The ID of the person who sold the estimate
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/{estimate_id}/sell"
    
    data = {"soldBy": sold_by}
    
    with httpx.Client() as client:
        response = client.put(url, headers=HEADERS, json=data)
        return response.json()

@mcp.tool()
def unsell_estimate(estimate_id: int) -> dict:
    """
    Mark an estimate as unsold.
    
    Args:
        estimate_id: The ID of the estimate to unsell
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/{estimate_id}/unsell"
    
    with httpx.Client() as client:
        response = client.put(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def dismiss_estimate(estimate_id: int) -> dict:
    """
    Dismiss an estimate.
    
    Args:
        estimate_id: The ID of the estimate to dismiss
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/{estimate_id}/dismiss"
    
    with httpx.Client() as client:
        response = client.put(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def add_estimate_item(estimate_id: int, item_data: dict) -> dict:
    """
    Add or update an item in an estimate.
    
    Args:
        estimate_id: The ID of the estimate to add the item to
        item_data: The item data containing skuId, quantity, unitPrice, description, etc.
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/{estimate_id}/items"
    
    with httpx.Client() as client:
        response = client.put(url, headers=HEADERS, json=item_data)
        return response.json()

@mcp.tool()
def delete_estimate_item(estimate_id: int, item_id: int) -> dict:
    """
    Delete an item from an estimate.
    
    Args:
        estimate_id: The ID of the estimate
        item_id: The ID of the item to delete
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/{estimate_id}/items/{item_id}"
    
    with httpx.Client() as client:
        response = client.delete(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def export_estimates(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export estimates feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/sales/v2/tenant/{TENANT_ID}/estimates/export"
    
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