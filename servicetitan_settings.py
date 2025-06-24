from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("ServiceTitan Settings API")

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
def get_employees(ids: Optional[str] = None, user_ids: Optional[str] = None, name: Optional[str] = None,
                 email: Optional[str] = None, active: Optional[str] = None, page: Optional[int] = None,
                 page_size: Optional[int] = None, include_total: Optional[bool] = None,
                 created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                 modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None) -> dict:
    """
    Get a list of employees with optional filtering.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        user_ids: Perform lookup by multiple User Ids (maximum 50)
        name: Filters records by name (case-insensitive "contains" operation)
        email: Filters records by email (exact match)
        active: What kind of items should be returned (True, Any, False)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/employees"
    
    params = {}
    if ids is not None:
        params["ids"] = ids
    if user_ids is not None:
        params["userIds"] = user_ids
    if name is not None:
        params["name"] = name
    if email is not None:
        params["email"] = email
    if active is not None:
        params["active"] = active
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
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def create_employee(employee_data: dict) -> dict:
    """
    Create a new employee.
    
    Args:
        employee_data: Employee data containing name, email, login, password, businessUnitId, roleId, etc.
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/employees"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=employee_data)
        return response.json()

@mcp.tool()
def get_employee(employee_id: int) -> dict:
    """
    Get a specific employee by ID.
    
    Args:
        employee_id: The ID of the employee to retrieve
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/employees/{employee_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def update_employee(employee_id: int, employee_data: dict) -> dict:
    """
    Update an existing employee.
    
    Args:
        employee_id: The ID of the employee to update
        employee_data: Employee data containing fields to update
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/employees/{employee_id}"
    
    with httpx.Client() as client:
        response = client.patch(url, headers=HEADERS, json=employee_data)
        return response.json()

@mcp.tool()
def perform_employee_account_action(employee_id: int, action_data: dict) -> dict:
    """
    Perform standard actions with an employee account.
    
    Args:
        employee_id: The ID of the employee
        action_data: Action data containing the action to perform
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/employees/{employee_id}/account-actions"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=action_data)
        return response.json()

@mcp.tool()
def export_employees(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export employees feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/export/employees"
    
    params = {}
    if from_token is not None:
        params["from"] = from_token
    if include_recent_changes is not None:
        params["includeRecentChanges"] = include_recent_changes
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def export_technicians(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export technicians feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/export/technicians"
    
    params = {}
    if from_token is not None:
        params["from"] = from_token
    if include_recent_changes is not None:
        params["includeRecentChanges"] = include_recent_changes
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_technicians(ids: Optional[str] = None, user_ids: Optional[str] = None, name: Optional[str] = None,
                   active: Optional[str] = None, page: Optional[int] = None, page_size: Optional[int] = None,
                   include_total: Optional[bool] = None, created_before: Optional[str] = None,
                   created_on_or_after: Optional[str] = None, modified_before: Optional[str] = None,
                   modified_on_or_after: Optional[str] = None) -> dict:
    """
    Get a list of technicians with optional filtering.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        user_ids: Perform lookup by multiple User Ids (maximum 50)
        name: Filters records by name (case-insensitive "contains" operation)
        active: What kind of items should be returned (True, Any, False)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/technicians"
    
    params = {}
    if ids is not None:
        params["ids"] = ids
    if user_ids is not None:
        params["userIds"] = user_ids
    if name is not None:
        params["name"] = name
    if active is not None:
        params["active"] = active
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
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def create_technician(technician_data: dict) -> dict:
    """
    Create a new technician.
    
    Args:
        technician_data: Technician data containing name, email, login, password, businessUnitId, roleId, etc.
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/technicians"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=technician_data)
        return response.json()

@mcp.tool()
def get_technician(technician_id: int) -> dict:
    """
    Get a specific technician by ID.
    
    Args:
        technician_id: The ID of the technician to retrieve
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/technicians/{technician_id}"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def update_technician(technician_id: int, technician_data: dict) -> dict:
    """
    Update an existing technician.
    
    Args:
        technician_id: The ID of the technician to update
        technician_data: Technician data containing fields to update
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/technicians/{technician_id}"
    
    with httpx.Client() as client:
        response = client.patch(url, headers=HEADERS, json=technician_data)
        return response.json()

@mcp.tool()
def perform_technician_account_action(technician_id: int, action_data: dict) -> dict:
    """
    Perform standard actions with a technician account.
    
    Args:
        technician_id: The ID of the technician
        action_data: Action data containing the action to perform, licenseType, truckId
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/technicians/{technician_id}/account-actions"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=action_data)
        return response.json()

@mcp.tool()
def get_user_roles(ids: Optional[str] = None, name: Optional[str] = None, active: Optional[str] = None,
                  page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None,
                  created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                  employee_type: Optional[str] = None) -> dict:
    """
    Get a list of user roles with optional filtering.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        name: Filters records by name (case-insensitive "contains" operation)
        active: What kind of items should be returned (True, Any, False)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        employee_type: Filter roles by employee type (None, Employee, Technician, All)
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/user-roles"
    
    params = {}
    if ids is not None:
        params["ids"] = ids
    if name is not None:
        params["name"] = name
    if active is not None:
        params["active"] = active
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
    if employee_type is not None:
        params["employeeType"] = employee_type
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_business_units(ids: Optional[str] = None, name: Optional[str] = None, active: Optional[str] = None,
                      page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None,
                      created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
                      modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
                      external_data_application_guid: Optional[str] = None) -> dict:
    """
    Get a list of business units with optional filtering.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        name: Filters records by name (case-insensitive "contains" operation)
        active: What kind of items should be returned (True, Any, False)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        external_data_application_guid: GUID for filtering external data
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/business-units"
    
    params = {}
    if ids is not None:
        params["ids"] = ids
    if name is not None:
        params["name"] = name
    if active is not None:
        params["active"] = active
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
    if external_data_application_guid is not None:
        params["externalDataApplicationGuid"] = external_data_application_guid
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_business_unit(business_unit_id: int, external_data_application_guid: Optional[str] = None) -> dict:
    """
    Get a specific business unit by ID.
    
    Args:
        business_unit_id: The ID of the business unit to retrieve
        external_data_application_guid: Optional GUID for filtering external data
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/business-units/{business_unit_id}"
    
    params = {}
    if external_data_application_guid is not None:
        params["externalDataApplicationGuid"] = external_data_application_guid
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def update_business_unit(business_unit_id: int, business_unit_data: dict) -> dict:
    """
    Update an existing business unit.
    
    Args:
        business_unit_id: The ID of the business unit to update
        business_unit_data: Business unit data containing external data to update
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/business-units/{business_unit_id}"
    
    with httpx.Client() as client:
        response = client.patch(url, headers=HEADERS, json=business_unit_data)
        return response.json()

@mcp.tool()
def export_business_units(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export business units feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/export/business-units"
    
    params = {}
    if from_token is not None:
        params["from"] = from_token
    if include_recent_changes is not None:
        params["includeRecentChanges"] = include_recent_changes
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def export_tag_types(from_token: Optional[str] = None, include_recent_changes: Optional[bool] = None) -> dict:
    """
    Export tag types feed for bulk data retrieval.
    
    Args:
        from_token: Continuation token received from previous export request or custom date string
        include_recent_changes: Use true to start receiving the most recent changes quicker
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/export/tag-types"
    
    params = {}
    if from_token is not None:
        params["from"] = from_token
    if include_recent_changes is not None:
        params["includeRecentChanges"] = include_recent_changes
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def get_tag_types(page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None,
                 active: Optional[str] = None, created_before: Optional[str] = None,
                 created_on_or_after: Optional[str] = None, modified_before: Optional[str] = None,
                 modified_on_or_after: Optional[str] = None, sort: Optional[str] = None) -> dict:
    """
    Get a list of tag types with optional filtering.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        active: What kind of items should be returned (True, Any, False)
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        sort: Sort order for results
    """
    url = f"{BASE_URL}/settings/v2/tenant/{TENANT_ID}/tag-types"
    
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["pageSize"] = page_size
    if include_total is not None:
        params["includeTotal"] = include_total
    if active is not None:
        params["active"] = active
    if created_before is not None:
        params["createdBefore"] = created_before
    if created_on_or_after is not None:
        params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None:
        params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None:
        params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None:
        params["sort"] = sort
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 