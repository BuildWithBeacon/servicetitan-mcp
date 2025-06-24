from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("ServiceTitan Reporting API")

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
def get_dynamic_value_set(dynamic_set_id: str, page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None) -> dict:
    """
    List values of given dynamic set including key and display name.
    
    Args:
        dynamic_set_id: ID of dynamic set taken from a report description
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
    """
    url = f"{BASE_URL}/reporting/v2/tenant/{TENANT_ID}/dynamic-value-sets/{dynamic_set_id}"
    
    params = {}
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
def get_report_categories(page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None) -> dict:
    """
    List categories for existing reports.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
    """
    url = f"{BASE_URL}/reporting/v2/tenant/{TENANT_ID}/report-categories"
    
    params = {}
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
def get_reports_in_category(report_category: str, page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None) -> dict:
    """
    List reports within given category.
    
    Args:
        report_category: ID of category taken from the category list endpoint
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
    """
    url = f"{BASE_URL}/reporting/v2/tenant/{TENANT_ID}/report-category/{report_category}/reports"
    
    params = {}
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
def get_report_description(report_category: str, report_id: int) -> dict:
    """
    Get report description including input parameters and output fields etc.
    Note that the report description isn't fixed and may be changed by the report owner.
    
    Args:
        report_category: ID of category taken from the category list endpoint
        report_id: ID of report within the category
    """
    url = f"{BASE_URL}/reporting/v2/tenant/{TENANT_ID}/report-category/{report_category}/reports/{report_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def get_report_data(report_category: str, report_id: int, parameters: List[dict], page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None) -> dict:
    """
    Get report data. The result is based on current report description which isn't constant in general.
    Beware that report columns may be changed. Result field names are listed alongside the data in the response
    to validate that all the requested columns are there.
    
    Args:
        report_category: ID of category taken from the category list endpoint
        report_id: ID of report within the category
        parameters: List of parameter objects with 'name' and 'value' fields
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (1000 by default)
        include_total: Whether total count should be returned
    """
    url = f"{BASE_URL}/reporting/v2/tenant/{TENANT_ID}/report-category/{report_category}/reports/{report_id}/data"
    
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if include_total is not None:
        params["includeTotal"] = include_total
    
    data = {"parameters": parameters}
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, params=params, json=data)
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 