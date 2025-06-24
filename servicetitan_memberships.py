import os
import logging
from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env values
load_dotenv()

# Initialize MCP app
mcp = FastMCP("ServiceTitan Memberships")

# Environment variables
CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")

# OAuth + API URLs
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
BASE_URL = f"https://api.servicetitan.io/memberships/v2/tenant/{TENANT_ID}"

async def get_access_token() -> str:
    """Fetch OAuth2 access token from ServiceTitan."""
    if not CLIENT_ID or not CLIENT_SECRET or not APP_KEY or not TENANT_ID:
        error_msg = "ERROR_ENV: One or more ServiceTitan environment variables are not set."
        raise ValueError(error_msg)

    async with httpx.AsyncClient() as client:
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        response = await client.post(TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()
        token_response_json = response.json()
        
        access_token = token_response_json.get("access_token")
        
        if not isinstance(access_token, str):
            error_msg = f"ERROR_TOKEN: access_token is not a string or is missing. Type: {type(access_token)}, Value: {access_token}"
            raise TypeError(error_msg)
            
        return access_token

def clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from parameters"""
    return {k: v for k, v in params.items() if v is not None}

@mcp.tool()
async def get_memberships(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None,
    active: Optional[str] = None,
    membership_type_ids: Optional[str] = None,
    statuses: Optional[str] = None,
    invoice_template_ids: Optional[str] = None,
    location_ids: Optional[str] = None,
    customer_ids: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    from_: Optional[str] = None,
    to: Optional[str] = None,
    duration_from: Optional[int] = None,
    duration_to: Optional[int] = None,
    billing_frequencies: Optional[str] = None
) -> dict:
    """
    Retrieve memberships from ServiceTitan.
    
    Args:
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
        ids: Lookup by multiple IDs (maximum 50)
        created_before: Return items created before date/time (RFC3339 format)
        created_on_or_after: Return items created on or after date/time (RFC3339 format)
        modified_before: Return items modified before date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after date/time (RFC3339 format)
        sort: Sort by field (+FieldName for ascending, -FieldName for descending)
        active: What kind of items should be returned ("True", "Any", "False")
        membership_type_ids: Filter by membership type IDs
        statuses: Filter by membership statuses
        invoice_template_ids: Filter by invoice template IDs
        location_ids: Filter by location IDs
        customer_ids: Filter by customer IDs
        business_unit_ids: Filter by business unit IDs
        from_: Filter memberships from this date
        to: Filter memberships to this date
        duration_from: Filter by minimum duration
        duration_to: Filter by maximum duration
        billing_frequencies: Filter by billing frequencies
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/memberships"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "ids": ids,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "sort": sort,
        "active": active,
        "membershipTypeIds": membership_type_ids,
        "statuses": statuses,
        "invoiceTemplateIds": invoice_template_ids,
        "locationIds": location_ids,
        "customerIds": customer_ids,
        "businessUnitIds": business_unit_ids,
        "from": from_,
        "to": to,
        "durationFrom": duration_from,
        "durationTo": duration_to,
        "billingFrequencies": billing_frequencies
    }

    clean_params_dict = clean_params(params)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params_dict)
        if response.status_code == 404:
            return {"error": "Memberships not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_membership_by_id(membership_id: str) -> dict:
    """
    Retrieve a specific membership by ID.
    
    Args:
        membership_id: The ID of the membership to retrieve
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/memberships/{membership_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": "Membership not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def sell_membership(
    customer_id: int,
    membership_type_id: int,
    invoice_template_id: int,
    location_id: int,
    business_unit_id: int,
    sold_by_id: int,
    sold_on: str,
    from_: str,
    to: str,
    duration: int,
    duration_type: str,
    billing_frequency: str,
    active: bool = True,
    external_data: Optional[dict] = None
) -> dict:
    """
    Sell a new membership.
    
    Args:
        customer_id: Customer ID for the membership
        membership_type_id: Type of membership
        invoice_template_id: Invoice template to use
        location_id: Location ID
        business_unit_id: Business unit ID
        sold_by_id: ID of person who sold the membership
        sold_on: Date membership was sold (RFC3339 format)
        from_: Membership start date (RFC3339 format)
        to: Membership end date (RFC3339 format)
        duration: Duration of membership
        duration_type: Type of duration (e.g., "Month", "Year")
        billing_frequency: How often to bill (e.g., "Monthly", "Annually")
        active: Whether membership is active
        external_data: Additional external data
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/memberships"

    data = {
        "customerId": customer_id,
        "membershipTypeId": membership_type_id,
        "invoiceTemplateId": invoice_template_id,
        "locationId": location_id,
        "businessUnitId": business_unit_id,
        "soldById": sold_by_id,
        "soldOn": sold_on,
        "from": from_,
        "to": to,
        "duration": duration,
        "durationType": duration_type,
        "billingFrequency": billing_frequency,
        "active": active
    }

    if external_data:
        data["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_membership(
    membership_id: str,
    from_: Optional[str] = None,
    to: Optional[str] = None,
    duration: Optional[int] = None,
    duration_type: Optional[str] = None,
    billing_frequency: Optional[str] = None,
    active: Optional[bool] = None,
    external_data: Optional[dict] = None
) -> dict:
    """
    Update an existing membership.
    
    Args:
        membership_id: ID of membership to update
        from_: New start date (RFC3339 format)
        to: New end date (RFC3339 format)
        duration: New duration
        duration_type: New duration type
        billing_frequency: New billing frequency
        active: New active status
        external_data: External data updates
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/memberships/{membership_id}"

    data = {}
    if from_ is not None:
        data["from"] = from_
    if to is not None:
        data["to"] = to
    if duration is not None:
        data["duration"] = duration
    if duration_type is not None:
        data["durationType"] = duration_type
    if billing_frequency is not None:
        data["billingFrequency"] = billing_frequency
    if active is not None:
        data["active"] = active
    if external_data is not None:
        data["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=data)
        if response.status_code == 404:
            return {"error": "Membership not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_membership_status_changes(
    membership_id: str,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Get status changes for a membership.
    
    Args:
        membership_id: ID of the membership
        page: Page number to return
        page_size: Number of records to return
        include_total: Whether to include total count
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/memberships/{membership_id}/status-changes"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }

    clean_params_dict = clean_params(params)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params_dict)
        if response.status_code == 404:
            return {"error": "Membership not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_membership_types(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None,
    active: Optional[str] = None
) -> dict:
    """
    Get membership types.
    
    Args:
        page: Page number to return
        page_size: Number of records to return
        include_total: Whether to include total count
        ids: Filter by specific IDs
        created_before: Filter by creation date
        created_on_or_after: Filter by creation date
        modified_before: Filter by modification date
        modified_on_or_after: Filter by modification date
        sort: Sort order
        active: Filter by active status
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/membership-types"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "ids": ids,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "sort": sort,
        "active": active
    }

    clean_params_dict = clean_params(params)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params_dict)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_recurring_services(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None,
    active: Optional[str] = None,
    membership_ids: Optional[str] = None
) -> dict:
    """
    Get recurring services.
    
    Args:
        page: Page number to return
        page_size: Number of records to return
        include_total: Whether to include total count
        ids: Filter by specific IDs
        created_before: Filter by creation date
        created_on_or_after: Filter by creation date
        modified_before: Filter by modification date
        modified_on_or_after: Filter by modification date
        sort: Sort order
        active: Filter by active status
        membership_ids: Filter by membership IDs
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/recurring-services"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "ids": ids,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "sort": sort,
        "active": active,
        "membershipIds": membership_ids
    }

    clean_params_dict = clean_params(params)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params_dict)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_recurring_service_events(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None,
    recurring_service_ids: Optional[str] = None,
    membership_ids: Optional[str] = None,
    statuses: Optional[str] = None,
    from_: Optional[str] = None,
    to: Optional[str] = None
) -> dict:
    """
    Get recurring service events.
    
    Args:
        page: Page number to return
        page_size: Number of records to return
        include_total: Whether to include total count
        ids: Filter by specific IDs
        created_before: Filter by creation date
        created_on_or_after: Filter by creation date
        modified_before: Filter by modification date
        modified_on_or_after: Filter by modification date
        sort: Sort order
        recurring_service_ids: Filter by recurring service IDs
        membership_ids: Filter by membership IDs
        statuses: Filter by event statuses
        from_: Filter events from date
        to: Filter events to date
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/recurring-service-events"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "ids": ids,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "sort": sort,
        "recurringServiceIds": recurring_service_ids,
        "membershipIds": membership_ids,
        "statuses": statuses,
        "from": from_,
        "to": to
    }

    clean_params_dict = clean_params(params)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params_dict)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def mark_recurring_service_event_complete(event_id: str) -> dict:
    """
    Mark a recurring service event as complete.
    
    Args:
        event_id: ID of the event to mark complete
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/recurring-service-events/{event_id}/mark-complete"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        if response.status_code == 404:
            return {"error": "Recurring service event not found"}
        response.raise_for_status()
        return {"message": "Event marked as complete"}

@mcp.tool()
async def mark_recurring_service_event_incomplete(event_id: str) -> dict:
    """
    Mark a recurring service event as incomplete.
    
    Args:
        event_id: ID of the event to mark incomplete
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/recurring-service-events/{event_id}/mark-incomplete"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        if response.status_code == 404:
            return {"error": "Recurring service event not found"}
        response.raise_for_status()
        return {"message": "Event marked as incomplete"}

@mcp.tool()
async def export_memberships() -> dict:
    """Export memberships data."""
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/export/memberships"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_membership_types() -> dict:
    """Export membership types data."""
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/export/membership-types"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_recurring_services() -> dict:
    """Export recurring services data."""
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/export/recurring-services"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_recurring_service_events() -> dict:
    """Export recurring service events data."""
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/export/recurring-service-events"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 