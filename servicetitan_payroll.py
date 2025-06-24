from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional, List

# Load .env values
load_dotenv()

# Env vars
CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")

# OAuth + API URLs
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
PAYROLL_BASE_URL = "https://api.servicetitan.io/payroll/v2"

# FastMCP instance for Payroll v2 API
mcp = FastMCP("servicetitan-payroll")

async def get_access_token() -> str:
    """Fetch OAuth2 access token from ServiceTitan."""
    if not CLIENT_ID or not CLIENT_SECRET or not APP_KEY or not TENANT_ID:
        error_msg = "ERROR_ENV: One or more ServiceTitan environment variables are not set."
        raise Exception(error_msg)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        return response.json()["access_token"]

# EXPORT ENDPOINTS

@mcp.tool()
async def export_job_splits(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> dict:
    """Provides export feed for job splits."""
    access_token = await get_access_token()
    
    params = {}
    if from_token is not None: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/export/jobs/splits",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_payroll_adjustments(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> dict:
    """Provides export feed for payroll adjustments."""
    access_token = await get_access_token()
    
    params = {}
    if from_token is not None: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/export/payroll-adjustments",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_job_timesheets(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> dict:
    """Provides export feed for job timesheets."""
    access_token = await get_access_token()
    
    params = {}
    if from_token is not None: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/export/jobs/timesheets",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_activity_codes(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> dict:
    """Provides export feed for activity codes."""
    access_token = await get_access_token()
    
    params = {}
    if from_token is not None: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/export/activity-codes",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_timesheet_codes(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> dict:
    """Provides export feed for timesheet codes."""
    access_token = await get_access_token()
    
    params = {}
    if from_token is not None: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/export/timesheet-codes",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_gross_pay_items(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> dict:
    """Provides export feed for gross pay items."""
    access_token = await get_access_token()
    
    params = {}
    if from_token is not None: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/export/gross-pay-items",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_payroll_settings(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> dict:
    """Provides export feed for payroll settings."""
    access_token = await get_access_token()
    
    params = {}
    if from_token is not None: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/export/payroll-settings",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# GROSS PAY ITEMS ENDPOINTS

@mcp.tool()
async def create_gross_pay_item(
    payroll_id: int,
    amount: float,
    activity_code_id: int,
    date: str,
    invoice_id: Optional[int] = None,
    memo: Optional[str] = None
) -> dict:
    """Creates new gross pay item."""
    access_token = await get_access_token()
    
    body = {
        "payrollId": payroll_id,
        "amount": amount,
        "activityCodeId": activity_code_id,
        "date": date
    }
    if invoice_id is not None: body["invoiceId"] = invoice_id
    if memo is not None: body["memo"] = memo
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/gross-pay-items",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_gross_pay_items(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    employee_type: Optional[str] = None,
    employee_id: Optional[int] = None,
    payroll_ids: Optional[str] = None,
    date_on_or_after: Optional[str] = None,
    date_on_or_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_on_or_before: Optional[str] = None
) -> dict:
    """Gets a list of gross pay items."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if employee_type is not None: params["employeeType"] = employee_type
    if employee_id is not None: params["employeeId"] = employee_id
    if payroll_ids is not None: params["payrollIds"] = payroll_ids
    if date_on_or_after is not None: params["dateOnOrAfter"] = date_on_or_after
    if date_on_or_before is not None: params["dateOnOrBefore"] = date_on_or_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if modified_on_or_before is not None: params["modifiedOnOrBefore"] = modified_on_or_before
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/gross-pay-items",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_gross_pay_item(
    item_id: int,
    payroll_id: int,
    amount: float,
    activity_code_id: int,
    date: str,
    invoice_id: Optional[int] = None,
    memo: Optional[str] = None
) -> dict:
    """Update specified gross pay item."""
    access_token = await get_access_token()
    
    body = {
        "payrollId": payroll_id,
        "amount": amount,
        "activityCodeId": activity_code_id,
        "date": date
    }
    if invoice_id is not None: body["invoiceId"] = invoice_id
    if memo is not None: body["memo"] = memo
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/gross-pay-items/{item_id}",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_gross_pay_item(item_id: int) -> dict:
    """Delete specified gross pay item."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/gross-pay-items/{item_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return {"success": True}

# JOB SPLITS ENDPOINTS

@mcp.tool()
async def get_job_splits(
    job_id: int,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    active: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of job splits."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if created_before is not None: params["createdBefore"] = created_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if active is not None: params["active"] = active
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/jobs/{job_id}/splits",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_splits_by_multiple_jobs(
    job_ids: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    active: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of job splits by multiple jobs."""
    access_token = await get_access_token()
    
    params = {}
    if job_ids is not None: params["jobIds"] = job_ids
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if created_before is not None: params["createdBefore"] = created_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if active is not None: params["active"] = active
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/jobs/splits",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# LOCATION RATES ENDPOINTS

@mcp.tool()
async def get_location_rates(
    location_ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    active: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of location hourly rates by multiple locations."""
    access_token = await get_access_token()
    
    params = {}
    if location_ids is not None: params["locationIds"] = location_ids
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if active is not None: params["active"] = active
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/locations/rates",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# ACTIVITY CODES ENDPOINTS

@mcp.tool()
async def get_activity_codes(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None
) -> dict:
    """Gets a list of payroll activity codes."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/activity-codes",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_activity_code_by_id(activity_code_id: int) -> dict:
    """Gets payroll activity code specified by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/activity-codes/{activity_code_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# PAYROLL ADJUSTMENTS ENDPOINTS

@mcp.tool()
async def create_payroll_adjustment(
    employee_type: str,
    employee_id: int,
    posted_on: str,
    amount: float,
    memo: str,
    activity_code_id: int,
    invoice_id: Optional[int] = None,
    hours: Optional[float] = None,
    rate: Optional[float] = None
) -> dict:
    """Creates new payroll adjustment."""
    access_token = await get_access_token()
    
    body = {
        "employeeType": employee_type,
        "employeeId": employee_id,
        "postedOn": posted_on,
        "amount": amount,
        "memo": memo,
        "activityCodeId": activity_code_id
    }
    if invoice_id is not None: body["invoiceId"] = invoice_id
    if hours is not None: body["hours"] = hours
    if rate is not None: body["rate"] = rate
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/payroll-adjustments",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_payroll_adjustments(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    employee_ids: Optional[str] = None,
    posted_on_or_after: Optional[str] = None,
    posted_on_or_before: Optional[str] = None
) -> dict:
    """Gets a list of payroll adjustments."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if employee_ids is not None: params["employeeIds"] = employee_ids
    if posted_on_or_after is not None: params["postedOnOrAfter"] = posted_on_or_after
    if posted_on_or_before is not None: params["postedOnOrBefore"] = posted_on_or_before
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/payroll-adjustments",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_payroll_adjustment_by_id(
    adjustment_id: int,
    employee_type: Optional[str] = None
) -> dict:
    """Gets payroll adjustment specified by ID."""
    access_token = await get_access_token()
    
    params = {}
    if employee_type is not None: params["employeeType"] = employee_type
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/payroll-adjustments/{adjustment_id}",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# PAYROLLS ENDPOINTS

@mcp.tool()
async def get_payrolls(
    employee_type: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    started_on_or_after: Optional[str] = None,
    ended_on_or_before: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    approved_on_or_after: Optional[str] = None,
    status: Optional[str] = None,
    active: Optional[str] = None
) -> dict:
    """Gets a list of payrolls."""
    access_token = await get_access_token()
    
    params = {}
    if employee_type is not None: params["employeeType"] = employee_type
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if started_on_or_after is not None: params["startedOnOrAfter"] = started_on_or_after
    if ended_on_or_before is not None: params["endedOnOrBefore"] = ended_on_or_before
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if approved_on_or_after is not None: params["approvedOnOrAfter"] = approved_on_or_after
    if status is not None: params["status"] = status
    if active is not None: params["active"] = active
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/payrolls",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_technician_payrolls(
    technician_id: int,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    started_on_or_after: Optional[str] = None,
    ended_on_or_before: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    approved_on_or_after: Optional[str] = None,
    status: Optional[str] = None,
    active: Optional[str] = None
) -> dict:
    """Gets a list of technician payrolls."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if started_on_or_after is not None: params["startedOnOrAfter"] = started_on_or_after
    if ended_on_or_before is not None: params["endedOnOrBefore"] = ended_on_or_before
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if approved_on_or_after is not None: params["approvedOnOrAfter"] = approved_on_or_after
    if status is not None: params["status"] = status
    if active is not None: params["active"] = active
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/technicians/{technician_id}/payrolls",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_employee_payrolls(
    employee_id: int,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    started_on_or_after: Optional[str] = None,
    ended_on_or_before: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    approved_on_or_after: Optional[str] = None,
    status: Optional[str] = None,
    active: Optional[str] = None
) -> dict:
    """Gets a list of employee payrolls."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if started_on_or_after is not None: params["startedOnOrAfter"] = started_on_or_after
    if ended_on_or_before is not None: params["endedOnOrBefore"] = ended_on_or_before
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if approved_on_or_after is not None: params["approvedOnOrAfter"] = approved_on_or_after
    if status is not None: params["status"] = status
    if active is not None: params["active"] = active
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/employees/{employee_id}/payrolls",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# PAYROLL SETTINGS ENDPOINTS

@mcp.tool()
async def get_payroll_settings(
    employee_type: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    active: Optional[str] = None
) -> dict:
    """Gets the payroll settings list."""
    access_token = await get_access_token()
    
    params = {}
    if employee_type is not None: params["employeeType"] = employee_type
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if active is not None: params["active"] = active
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/payroll-settings",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_employee_payroll_settings(employee_id: int) -> dict:
    """Gets the employee payroll settings."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/employees/{employee_id}/payroll-settings",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_employee_payroll_settings(
    employee_id: int,
    external_payroll_id: Optional[str] = None,
    hourly_rate: Optional[float] = None,
    manager_id: Optional[int] = None,
    hire_date: Optional[str] = None
) -> dict:
    """Updates the employee payroll settings."""
    access_token = await get_access_token()
    
    body = {}
    if external_payroll_id is not None: body["externalPayrollId"] = external_payroll_id
    if hourly_rate is not None: body["hourlyRate"] = hourly_rate
    if manager_id is not None: body["managerId"] = manager_id
    if hire_date is not None: body["hireDate"] = hire_date
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/employees/{employee_id}/payroll-settings",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_technician_payroll_settings(technician_id: int) -> dict:
    """Gets the technician payroll settings."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/technicians/{technician_id}/payroll-settings",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_technician_payroll_settings(
    technician_id: int,
    external_payroll_id: Optional[str] = None,
    hourly_rate: Optional[float] = None,
    manager_id: Optional[int] = None,
    hire_date: Optional[str] = None
) -> dict:
    """Updates the technician payroll settings."""
    access_token = await get_access_token()
    
    body = {}
    if external_payroll_id is not None: body["externalPayrollId"] = external_payroll_id
    if hourly_rate is not None: body["hourlyRate"] = hourly_rate
    if manager_id is not None: body["managerId"] = manager_id
    if hire_date is not None: body["hireDate"] = hire_date
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/technicians/{technician_id}/payroll-settings",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# TIMESHEET CODES ENDPOINTS

@mcp.tool()
async def get_timesheet_codes(
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    active: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of timesheet codes."""
    access_token = await get_access_token()
    
    params = {}
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if active is not None: params["active"] = active
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/timesheet-codes",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_timesheet_code_by_id(timesheet_code_id: int) -> dict:
    """Gets timesheet code specified by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/timesheet-codes/{timesheet_code_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# JOB TIMESHEETS ENDPOINTS

@mcp.tool()
async def get_job_timesheets(
    job_id: int,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    technician_id: Optional[int] = None,
    started_on: Optional[str] = None,
    ended_on: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of job timesheets."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if technician_id is not None: params["technicianId"] = technician_id
    if started_on is not None: params["startedOn"] = started_on
    if ended_on is not None: params["endedOn"] = ended_on
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/jobs/{job_id}/timesheets",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_job_timesheet(
    job_id: int,
    appointment_id: int,
    technician_id: int,
    dispatched_on: Optional[str] = None,
    arrived_on: Optional[str] = None,
    canceled_on: Optional[str] = None,
    done_on: Optional[str] = None
) -> dict:
    """Creates new job timesheet."""
    access_token = await get_access_token()
    
    body = {
        "appointmentId": appointment_id,
        "technicianId": technician_id
    }
    if dispatched_on is not None: body["dispatchedOn"] = dispatched_on
    if arrived_on is not None: body["arrivedOn"] = arrived_on
    if canceled_on is not None: body["canceledOn"] = canceled_on
    if done_on is not None: body["doneOn"] = done_on
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/jobs/{job_id}/timesheets",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_job_timesheet(
    job_id: int,
    timesheet_id: int,
    appointment_id: int,
    technician_id: int,
    dispatched_on: Optional[str] = None,
    arrived_on: Optional[str] = None,
    canceled_on: Optional[str] = None,
    done_on: Optional[str] = None
) -> dict:
    """Update specified job timesheet."""
    access_token = await get_access_token()
    
    body = {
        "appointmentId": appointment_id,
        "technicianId": technician_id
    }
    if dispatched_on is not None: body["dispatchedOn"] = dispatched_on
    if arrived_on is not None: body["arrivedOn"] = arrived_on
    if canceled_on is not None: body["canceledOn"] = canceled_on
    if done_on is not None: body["doneOn"] = done_on
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/jobs/{job_id}/timesheets/{timesheet_id}",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_job_timesheets_by_multiple_jobs(
    job_ids: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    technician_id: Optional[int] = None,
    started_on: Optional[str] = None,
    ended_on: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of job timesheets by multiple jobs."""
    access_token = await get_access_token()
    
    params = {}
    if job_ids is not None: params["jobIds"] = job_ids
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if technician_id is not None: params["technicianId"] = technician_id
    if started_on is not None: params["startedOn"] = started_on
    if ended_on is not None: params["endedOn"] = ended_on
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/jobs/timesheets",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# NON-JOB TIMESHEETS ENDPOINTS

@mcp.tool()
async def get_non_job_timesheets(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    employee_id: Optional[int] = None,
    employee_type: Optional[str] = None,
    active: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of non job timesheets for employee."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if employee_id is not None: params["employeeId"] = employee_id
    if employee_type is not None: params["employeeType"] = employee_type
    if active is not None: params["active"] = active
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYROLL_BASE_URL}/tenant/{TENANT_ID}/non-job-timesheets",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 