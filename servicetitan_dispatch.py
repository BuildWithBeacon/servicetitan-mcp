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
DISPATCH_BASE_URL = "https://api.servicetitan.io/dispatch/v2"

# FastMCP instance for Dispatch v2 API
mcp = FastMCP("servicetitan-dispatch")

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

# APPOINTMENT ASSIGNMENTS ENDPOINTS

@mcp.tool()
async def get_appointment_assignments(
    ids: Optional[str] = None,
    appointment_ids: Optional[str] = None,
    job_id: Optional[int] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    sort: Optional[str] = None,
    active: Optional[str] = None
) -> dict:
    """Gets a list of appointment assignments with filtering options."""
    access_token = await get_access_token()
    
    params = {}
    if ids is not None: params["ids"] = ids
    if appointment_ids is not None: params["appointmentIds"] = appointment_ids
    if job_id is not None: params["jobId"] = job_id
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if sort is not None: params["sort"] = sort
    if active is not None: params["active"] = active
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/appointment-assignments",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def assign_technicians_to_appointment(
    job_appointment_id: int,
    technician_ids: List[int]
) -> dict:
    """Assigns the list of technicians to the appointment."""
    access_token = await get_access_token()
    
    body = {
        "jobAppointmentId": job_appointment_id,
        "technicianIds": technician_ids
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/appointment-assignments/assign-technicians",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def unassign_technicians_from_appointment(
    job_appointment_id: int,
    technician_ids: List[int]
) -> dict:
    """Unassigns the list of technicians from the appointment."""
    access_token = await get_access_token()
    
    body = {
        "jobAppointmentId": job_appointment_id,
        "technicianIds": technician_ids
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/appointment-assignments/unassign-technicians",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

# ARRIVAL WINDOWS ENDPOINTS

@mcp.tool()
async def get_arrival_windows(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    active: Optional[str] = None
) -> dict:
    """Gets a list of arrival windows with filtering options."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if active is not None: params["active"] = active
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/arrival-windows",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_arrival_window(
    start: str,
    duration: str,
    business_unit_ids: List[int]
) -> dict:
    """Creates a new arrival window."""
    access_token = await get_access_token()
    
    body = {
        "start": start,
        "duration": duration,
        "businessUnitIds": business_unit_ids
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/arrival-windows",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_arrival_window_by_id(id: int) -> dict:
    """Gets a specific arrival window by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/arrival-windows/{id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_arrival_window(
    id: int,
    start: Optional[str] = None,
    duration: Optional[str] = None,
    business_unit_ids: Optional[List[int]] = None
) -> dict:
    """Updates an existing arrival window."""
    access_token = await get_access_token()
    
    body = {}
    if start is not None: body["start"] = start
    if duration is not None: body["duration"] = duration
    if business_unit_ids is not None: body["businessUnitIds"] = business_unit_ids
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/arrival-windows/{id}",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def set_arrival_window_active_status(
    id: int,
    is_active: bool
) -> dict:
    """Sets the active status of an arrival window."""
    access_token = await get_access_token()
    
    body = {"isActive": is_active}
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/arrival-windows/{id}/activated",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return {"success": True, "message": "Arrival window status updated"}

@mcp.tool()
async def get_arrival_windows_configuration() -> dict:
    """Gets the arrival windows configuration."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/arrival-windows/configuration",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_arrival_windows_configuration(
    configuration: str
) -> dict:
    """Updates the arrival windows configuration."""
    access_token = await get_access_token()
    
    body = {"configuration": configuration}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/arrival-windows/configuration",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

# BUSINESS HOURS ENDPOINTS

@mcp.tool()
async def get_business_hours() -> dict:
    """Gets the business hours configuration."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/business-hours",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_business_hours(
    weekdays: List[dict],
    saturday: Optional[List[dict]] = None,
    sunday: Optional[List[dict]] = None
) -> dict:
    """Creates or updates business hours configuration."""
    access_token = await get_access_token()
    
    body = {"weekdays": weekdays}
    if saturday is not None: body["saturday"] = saturday
    if sunday is not None: body["sunday"] = sunday
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/business-hours",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

# CAPACITY ENDPOINTS

@mcp.tool()
async def get_capacity(
    starts_on_or_after: str,
    ends_on_or_before: str,
    business_unit_ids: Optional[List[int]] = None,
    job_type_id: Optional[int] = None,
    skill_based_availability: Optional[bool] = None
) -> dict:
    """Gets capacity information for scheduling."""
    access_token = await get_access_token()
    
    body = {
        "startsOnOrAfter": starts_on_or_after,
        "endsOnOrBefore": ends_on_or_before
    }
    if business_unit_ids is not None: body["businessUnitIds"] = business_unit_ids
    if job_type_id is not None: body["jobTypeId"] = job_type_id
    if skill_based_availability is not None: body["skillBasedAvailability"] = skill_based_availability
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/capacity",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# TEAMS ENDPOINTS

@mcp.tool()
async def get_teams(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    include_inactive: Optional[bool] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of teams with filtering options."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if include_inactive is not None: params["includeInactive"] = include_inactive
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if created_before is not None: params["createdBefore"] = created_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/teams",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_team(
    name: str,
    active: Optional[bool] = None
) -> dict:
    """Creates a new team."""
    access_token = await get_access_token()
    
    body = {"name": name}
    if active is not None: body["active"] = active
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/teams",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_team_by_id(id: int) -> dict:
    """Gets a specific team by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/teams/{id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_team(id: int) -> dict:
    """Deletes a team by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/teams/{id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return {"success": True, "message": f"Team {id} deleted successfully"}

# TECHNICIAN SHIFTS ENDPOINTS

@mcp.tool()
async def get_technician_shifts(
    starts_on_or_after: Optional[str] = None,
    ends_on_or_before: Optional[str] = None,
    shift_type: Optional[str] = None,
    technician_id: Optional[int] = None,
    title_contains: Optional[str] = None,
    note_contains: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    active: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of technician shifts with filtering options."""
    access_token = await get_access_token()
    
    params = {}
    if starts_on_or_after is not None: params["startsOnOrAfter"] = starts_on_or_after
    if ends_on_or_before is not None: params["endsOnOrBefore"] = ends_on_or_before
    if shift_type is not None: params["shiftType"] = shift_type
    if technician_id is not None: params["technicianId"] = technician_id
    if title_contains is not None: params["titleContains"] = title_contains
    if note_contains is not None: params["noteContains"] = note_contains
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if active is not None: params["active"] = active
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/technician-shifts",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_technician_shift(
    technician_ids: List[int],
    shift_type: str,
    title: str,
    start: str,
    end: str,
    note: Optional[str] = None,
    timesheet_code_id: Optional[int] = None,
    repeat_type: Optional[str] = None,
    repeat_end_date: Optional[str] = None,
    repeat_interval: Optional[int] = None,
    shift_days: Optional[str] = None
) -> dict:
    """Creates a new technician shift."""
    access_token = await get_access_token()
    
    body = {
        "technicianIds": technician_ids,
        "shiftType": shift_type,
        "title": title,
        "start": start,
        "end": end
    }
    if note is not None: body["note"] = note
    if timesheet_code_id is not None: body["timesheetCodeId"] = timesheet_code_id
    if repeat_type is not None: body["repeatType"] = repeat_type
    if repeat_end_date is not None: body["repeatEndDate"] = repeat_end_date
    if repeat_interval is not None: body["repeatInterval"] = repeat_interval
    if shift_days is not None: body["shiftDays"] = shift_days
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/technician-shifts",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_technician_shift_by_id(id: int) -> dict:
    """Gets a specific technician shift by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/technician-shifts/{id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_technician_shift(
    id: int,
    shift_type: Optional[str] = None,
    title: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    note: Optional[str] = None,
    timesheet_code_id: Optional[int] = None
) -> dict:
    """Updates an existing technician shift."""
    access_token = await get_access_token()
    
    body = {}
    if shift_type is not None: body["shiftType"] = shift_type
    if title is not None: body["title"] = title
    if start is not None: body["start"] = start
    if end is not None: body["end"] = end
    if note is not None: body["note"] = note
    if timesheet_code_id is not None: body["timesheetCodeId"] = timesheet_code_id
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/technician-shifts/{id}",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_technician_shift(id: int) -> dict:
    """Deletes a technician shift by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/technician-shifts/{id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

# ZONES ENDPOINTS

@mcp.tool()
async def get_zones(
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
    """Gets a list of zones with filtering options."""
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
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/zones",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_zone(
    name: str,
    zips: Optional[List[str]] = None,
    cities: Optional[List[str]] = None,
    territory_numbers: Optional[List[str]] = None,
    locn_numbers: Optional[List[str]] = None,
    service_days_enabled: Optional[bool] = None,
    service_days_ids: Optional[List[int]] = None,
    business_units: Optional[List[int]] = None
) -> dict:
    """Creates a new zone."""
    access_token = await get_access_token()
    
    body = {"name": name}
    if zips is not None: body["zips"] = zips
    if cities is not None: body["cities"] = cities
    if territory_numbers is not None: body["territoryNumbers"] = territory_numbers
    if locn_numbers is not None: body["locnNumbers"] = locn_numbers
    if service_days_enabled is not None: body["serviceDaysEnabled"] = service_days_enabled
    if service_days_ids is not None: body["serviceDaysIds"] = service_days_ids
    if business_units is not None: body["businessUnits"] = business_units
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/zones",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_zone_by_id(id: int) -> dict:
    """Gets a specific zone by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/zones/{id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_zone(
    zone_id: int,
    name: Optional[str] = None,
    zips: Optional[List[str]] = None,
    cities: Optional[List[str]] = None,
    territory_numbers: Optional[List[str]] = None,
    locn_numbers: Optional[List[str]] = None,
    service_days_enabled: Optional[bool] = None,
    service_days_ids: Optional[List[int]] = None,
    business_units: Optional[List[int]] = None
) -> dict:
    """Updates an existing zone."""
    access_token = await get_access_token()
    
    body = {}
    if name is not None: body["name"] = name
    if zips is not None: body["zips"] = zips
    if cities is not None: body["cities"] = cities
    if territory_numbers is not None: body["territoryNumbers"] = territory_numbers
    if locn_numbers is not None: body["locnNumbers"] = locn_numbers
    if service_days_enabled is not None: body["serviceDaysEnabled"] = service_days_enabled
    if service_days_ids is not None: body["serviceDaysIds"] = service_days_ids
    if business_units is not None: body["businessUnits"] = business_units
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/zones/{zone_id}",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_zone(zone_id: int) -> dict:
    """Deletes a zone by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/zones/{zone_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return {"success": True, "message": f"Zone {zone_id} deleted successfully"}

# NON-JOB APPOINTMENTS ENDPOINTS

@mcp.tool()
async def get_non_job_appointments(
    technician_id: Optional[int] = None,
    starts_on_or_after: Optional[str] = None,
    starts_on_or_before: Optional[str] = None,
    timesheet_code_id: Optional[int] = None,
    active_only: Optional[bool] = None,
    show_on_technician_schedule: Optional[bool] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    ids: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of non-job appointments with filtering options."""
    access_token = await get_access_token()
    
    params = {}
    if technician_id is not None: params["technicianId"] = technician_id
    if starts_on_or_after is not None: params["startsOnOrAfter"] = starts_on_or_after
    if starts_on_or_before is not None: params["startsOnOrBefore"] = starts_on_or_before
    if timesheet_code_id is not None: params["timesheetCodeId"] = timesheet_code_id
    if active_only is not None: params["activeOnly"] = active_only
    if show_on_technician_schedule is not None: params["showOnTechnicianSchedule"] = show_on_technician_schedule
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if created_before is not None: params["createdBefore"] = created_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if ids is not None: params["ids"] = ids
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/non-job-appointments",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_non_job_appointment(
    technician_id: int,
    start: str,
    duration: str,
    name: str,
    timesheet_code_id: Optional[int] = None,
    summary: Optional[str] = None,
    clear_dispatch_board: Optional[bool] = None,
    clear_technician_view: Optional[bool] = None,
    show_on_technician_schedule: Optional[bool] = None,
    remove_technician_from_capacity_planning: Optional[bool] = None,
    all_day: Optional[bool] = None,
    repeat: Optional[bool] = None,
    count_occurrences: Optional[int] = None,
    interval: Optional[int] = None,
    frequency: Optional[str] = None,
    end_type: Optional[str] = None,
    end_on: Optional[str] = None,
    days_of_week: Optional[str] = None
) -> dict:
    """Creates a new non-job appointment."""
    access_token = await get_access_token()
    
    body = {
        "technicianId": technician_id,
        "start": start,
        "duration": duration,
        "name": name
    }
    if timesheet_code_id is not None: body["timesheetCodeId"] = timesheet_code_id
    if summary is not None: body["summary"] = summary
    if clear_dispatch_board is not None: body["clearDispatchBoard"] = clear_dispatch_board
    if clear_technician_view is not None: body["clearTechnicianView"] = clear_technician_view
    if show_on_technician_schedule is not None: body["showOnTechnicianSchedule"] = show_on_technician_schedule
    if remove_technician_from_capacity_planning is not None: body["removeTechnicianFromCapacityPlanning"] = remove_technician_from_capacity_planning
    if all_day is not None: body["allDay"] = all_day
    if repeat is not None: body["repeat"] = repeat
    if count_occurrences is not None: body["countOccurrences"] = count_occurrences
    if interval is not None: body["interval"] = interval
    if frequency is not None: body["frequency"] = frequency
    if end_type is not None: body["endType"] = end_type
    if end_on is not None: body["endOn"] = end_on
    if days_of_week is not None: body["daysOfWeek"] = days_of_week
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/non-job-appointments",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_non_job_appointment_by_id(id: int) -> dict:
    """Gets a specific non-job appointment by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/non-job-appointments/{id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_non_job_appointment(
    id: int,
    technician_id: Optional[int] = None,
    start: Optional[str] = None,
    duration: Optional[str] = None,
    name: Optional[str] = None,
    timesheet_code_id: Optional[int] = None,
    summary: Optional[str] = None,
    clear_dispatch_board: Optional[bool] = None,
    clear_technician_view: Optional[bool] = None,
    show_on_technician_schedule: Optional[bool] = None,
    remove_technician_from_capacity_planning: Optional[bool] = None,
    all_day: Optional[bool] = None
) -> dict:
    """Updates an existing non-job appointment."""
    access_token = await get_access_token()
    
    body = {}
    if technician_id is not None: body["technicianId"] = technician_id
    if start is not None: body["start"] = start
    if duration is not None: body["duration"] = duration
    if name is not None: body["name"] = name
    if timesheet_code_id is not None: body["timesheetCodeId"] = timesheet_code_id
    if summary is not None: body["summary"] = summary
    if clear_dispatch_board is not None: body["clearDispatchBoard"] = clear_dispatch_board
    if clear_technician_view is not None: body["clearTechnicianView"] = clear_technician_view
    if show_on_technician_schedule is not None: body["showOnTechnicianSchedule"] = show_on_technician_schedule
    if remove_technician_from_capacity_planning is not None: body["removeTechnicianFromCapacityPlanning"] = remove_technician_from_capacity_planning
    if all_day is not None: body["allDay"] = all_day
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/non-job-appointments/{id}",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_non_job_appointment(id: int) -> dict:
    """Deletes a non-job appointment by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/non-job-appointments/{id}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        if response.status_code == 404:
            return {"error": "Not found", "status_code": 404}
        response.raise_for_status()
        return response.json()

# TECHNICIAN TRACKING ENDPOINT

@mcp.tool()
async def get_technician_tracking(
    technician_id: int,
    appointment_id: int
) -> dict:
    """Gets the technician tracking URL for a specific technician and appointment."""
    access_token = await get_access_token()
    
    params = {
        "technicianId": technician_id,
        "appointmentId": appointment_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/technician-tracking",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# EXPORT ENDPOINTS

@mcp.tool()
async def export_appointment_assignments(
    active: Optional[str] = None,
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> dict:
    """Provides export feed for appointment assignments."""
    access_token = await get_access_token()
    
    params = {}
    if active is not None: params["active"] = active
    if from_token is not None: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/export/appointment-assignments",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# GPS PROVIDER ENDPOINTS

@mcp.tool()
async def create_gps_pings(
    gps_provider: str,
    gps_pings: List[dict]
) -> dict:
    """Creates new GPS pings for the specified GPS provider."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/gps-provider/{gps_provider}/gps-pings",
            json=gps_pings,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# BULK OPERATIONS

@mcp.tool()
async def bulk_delete_technician_shifts(
    start: str,
    end: str
) -> dict:
    """Deletes technician shifts within the specified date range."""
    access_token = await get_access_token()
    
    body = {
        "start": start,
        "end": end
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{DISPATCH_BASE_URL}/tenant/{TENANT_ID}/technician-shifts/bulk-delete",
            json=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 