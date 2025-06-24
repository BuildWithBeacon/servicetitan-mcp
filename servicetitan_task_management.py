from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp = FastMCP("ServiceTitan Task Management API")

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
def get_client_side_data() -> dict:
    """
    Get client-side data including employees, business units, task priorities, resolution types, statuses, types, sources, and resolutions.
    This provides all the reference data needed for task management operations.
    """
    url = f"{BASE_URL}/taskmanagement/v2/tenant/{TENANT_ID}/data"
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS)
        return response.json()

@mcp.tool()
def get_tasks(page: Optional[int] = None, page_size: Optional[int] = None, include_total: Optional[bool] = None,
             active: Optional[str] = None, created_before: Optional[str] = None, created_on_or_after: Optional[str] = None,
             modified_before: Optional[str] = None, modified_on_or_after: Optional[str] = None,
             reported_before: Optional[str] = None, reported_on_or_after: Optional[str] = None,
             complete_before: Optional[str] = None, complete_on_or_after: Optional[str] = None,
             is_closed: Optional[bool] = None, statuses: Optional[str] = None, ids: Optional[str] = None,
             name: Optional[str] = None, include_subtasks: Optional[bool] = None,
             business_unit_ids: Optional[str] = None, employee_task_type_ids: Optional[str] = None,
             employee_task_source_ids: Optional[str] = None, employee_task_resolution_ids: Optional[str] = None,
             reported_by_id: Optional[int] = None, assigned_to_id: Optional[int] = None,
             involved_employee_id_list: Optional[str] = None, customer_id: Optional[int] = None,
             job_id: Optional[int] = None, project_id: Optional[int] = None, priorities: Optional[str] = None,
             task_number: Optional[int] = None, job_number: Optional[str] = None, sort: Optional[str] = None) -> dict:
    """
    Get a list of tasks with extensive filtering options.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        active: Active status filter (True, Any, False)
        created_before: Created date before (RFC3339 format)
        created_on_or_after: Created date on or after (RFC3339 format)
        modified_before: Modified date before (RFC3339 format)
        modified_on_or_after: Modified date on or after (RFC3339 format)
        reported_before: Reported date before (RFC3339 format)
        reported_on_or_after: Reported date on or after (RFC3339 format)
        complete_before: Completed before (RFC3339 format)
        complete_on_or_after: Completed on or after (RFC3339 format)
        is_closed: Is closed status (deprecated, use statuses instead)
        statuses: Task status filter
        ids: Task IDs (comma separated)
        name: Name filter
        include_subtasks: Include subtasks in results
        business_unit_ids: Business unit IDs (comma separated)
        employee_task_type_ids: Employee task type IDs (comma separated)
        employee_task_source_ids: Employee task source IDs (comma separated)
        employee_task_resolution_ids: Employee task resolution IDs (comma separated)
        reported_by_id: Reported by employee ID
        assigned_to_id: Assigned to employee ID
        involved_employee_id_list: Involved employee IDs (comma separated)
        customer_id: Customer ID filter
        job_id: Job ID filter
        project_id: Project ID filter
        priorities: Priorities filter (comma separated)
        task_number: Task number filter
        job_number: Job number filter
        sort: Sort order (+FieldName for ascending, -FieldName for descending)
    """
    url = f"{BASE_URL}/taskmanagement/v2/tenant/{TENANT_ID}/tasks"
    
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
    if reported_before is not None:
        params["reportedBefore"] = reported_before
    if reported_on_or_after is not None:
        params["reportedOnOrAfter"] = reported_on_or_after
    if complete_before is not None:
        params["completeBefore"] = complete_before
    if complete_on_or_after is not None:
        params["completeOnOrAfter"] = complete_on_or_after
    if is_closed is not None:
        params["isClosed"] = is_closed
    if statuses is not None:
        params["statuses"] = statuses
    if ids is not None:
        params["ids"] = ids
    if name is not None:
        params["name"] = name
    if include_subtasks is not None:
        params["includeSubtasks"] = include_subtasks
    if business_unit_ids is not None:
        params["businessUnitIds"] = business_unit_ids
    if employee_task_type_ids is not None:
        params["employeeTaskTypeIds"] = employee_task_type_ids
    if employee_task_source_ids is not None:
        params["employeeTaskSourceIds"] = employee_task_source_ids
    if employee_task_resolution_ids is not None:
        params["employeeTaskResolutionIds"] = employee_task_resolution_ids
    if reported_by_id is not None:
        params["reportedById"] = reported_by_id
    if assigned_to_id is not None:
        params["assignedToId"] = assigned_to_id
    if involved_employee_id_list is not None:
        params["involvedEmployeeIdList"] = involved_employee_id_list
    if customer_id is not None:
        params["customerId"] = customer_id
    if job_id is not None:
        params["jobId"] = job_id
    if project_id is not None:
        params["projectId"] = project_id
    if priorities is not None:
        params["priorities"] = priorities
    if task_number is not None:
        params["taskNumber"] = task_number
    if job_number is not None:
        params["jobNumber"] = job_number
    if sort is not None:
        params["sort"] = sort
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def create_task(task_data: dict) -> dict:
    """
    Create a new task.
    
    Args:
        task_data: Task data containing reportedById, assignedToId, name, businessUnitId, 
                  employeeTaskTypeId, employeeTaskSourceId, description, priority, etc.
    """
    url = f"{BASE_URL}/taskmanagement/v2/tenant/{TENANT_ID}/tasks"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=task_data)
        return response.json()

@mcp.tool()
def get_task(task_id: int, include_subtasks: Optional[bool] = None) -> dict:
    """
    Get a specific task by ID.
    
    Args:
        task_id: The ID of the task to retrieve
        include_subtasks: Whether to include subtasks in the response
    """
    url = f"{BASE_URL}/taskmanagement/v2/tenant/{TENANT_ID}/tasks/{task_id}"
    
    params = {}
    if include_subtasks is not None:
        params["includeSubtasks"] = include_subtasks
    
    with httpx.Client() as client:
        response = client.get(url, headers=HEADERS, params=params)
        return response.json()

@mcp.tool()
def create_subtask(task_id: int, subtask_data: dict) -> dict:
    """
    Create a subtask for an existing task.
    
    Args:
        task_id: The ID of the parent task
        subtask_data: Subtask data containing name, assignedToId, dueDateTime, isClosed
    """
    url = f"{BASE_URL}/taskmanagement/v2/tenant/{TENANT_ID}/tasks/{task_id}/subtasks"
    
    with httpx.Client() as client:
        response = client.post(url, headers=HEADERS, json=subtask_data)
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 