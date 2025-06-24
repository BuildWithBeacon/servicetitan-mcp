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
mcp = FastMCP("ServiceTitan Marketing")

# Environment variables
CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")

# OAuth + API URLs
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
BASE_URL = f"https://api.servicetitan.io/marketing/v2/tenant/{TENANT_ID}"

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
async def get_categories(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """
    Gets a paginated list of campaign categories from ServiceTitan Marketing API.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (RFC3339 format)
        created_on_or_after: Return items created on or after certain date/time (RFC3339 format)
        sort: Applies sorting by field (+FieldName ascending, -FieldName descending).
              Available fields: Id, CreatedOn, Name
    
    Returns:
        dict: JSON response containing campaign categories with fields:
              - id: Category ID
              - name: Category name
              - active: Whether the category is active
              - type: Category type (e.g., "Regular")
              - createdOn: Creation timestamp
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/categories"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": "Categories not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_category(name: str) -> dict:
    """
    Creates a new campaign category in ServiceTitan Marketing API.
    
    Args:
        name: Name of the campaign category (required)
    
    Returns:
        dict: JSON response containing the created category ID
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/categories"
    
    data = {"name": name}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 400:
            return {"error": "Bad request - check category data"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_category_by_id(category_id: str) -> dict:
    """
    Gets a specific campaign category by ID from ServiceTitan Marketing API.
    
    Args:
        category_id: The ID of the category to retrieve (required)
    
    Returns:
        dict: JSON response containing category details with fields:
              - id: Category ID
              - name: Category name
              - active: Whether the category is active
              - type: Category type
              - createdOn: Creation timestamp
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/categories/{category_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Category with ID {category_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_category(
    category_id: str,
    name: Optional[str] = None,
    active: Optional[bool] = None
) -> dict:
    """
    Updates a specific campaign category in ServiceTitan Marketing API.
    
    Args:
        category_id: The ID of the category to update (required)
        name: New name for the category
        active: Whether the category should be active
    
    Returns:
        dict: JSON response containing the updated category ID
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/categories/{category_id}"
    
    data = {}
    if name is not None:
        data["name"] = name
    if active is not None:
        data["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=data)
        if response.status_code == 404:
            return {"error": f"Category with ID {category_id} not found"}
        if response.status_code == 400:
            return {"error": "Bad request - check category data"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_costs(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    year: Optional[int] = None,
    month: Optional[int] = None,
    campaign_id: Optional[int] = None,
    sort: Optional[str] = None
) -> dict:
    """
    Gets a paginated list of campaign costs from ServiceTitan Marketing API.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        year: Filter by year
        month: Filter by month
        campaign_id: Filter by campaign ID
        sort: Applies sorting by field (+FieldName ascending, -FieldName descending).
              Available fields: Id, Date (Year + Month)
    
    Returns:
        dict: JSON response containing campaign costs with fields:
              - id: Cost ID
              - year: Year of the cost
              - month: Month of the cost
              - dailyCost: Daily cost amount
              - campaignId: Associated campaign ID
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/costs"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "year": year,
        "month": month,
        "campaignId": campaign_id,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": "Costs not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_cost(
    campaign_id: int,
    year: int,
    month: int,
    daily_cost: float
) -> dict:
    """
    Creates a new campaign cost in ServiceTitan Marketing API.
    
    Args:
        campaign_id: ID of the campaign (required)
        year: Year for the cost (required)
        month: Month for the cost (required)
        daily_cost: Daily cost amount (required)
    
    Returns:
        dict: JSON response containing the created cost details
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/costs"
    
    data = {
        "campaignId": campaign_id,
        "year": year,
        "month": month,
        "dailyCost": daily_cost
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 400:
            return {"error": "Bad request - check cost data"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_cost_by_id(cost_id: str) -> dict:
    """
    Gets a specific campaign cost by ID from ServiceTitan Marketing API.
    
    Args:
        cost_id: The ID of the cost to retrieve (required)
    
    Returns:
        dict: JSON response containing cost details with fields:
              - id: Cost ID
              - year: Year of the cost
              - month: Month of the cost
              - dailyCost: Daily cost amount
              - campaignId: Associated campaign ID
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/costs/{cost_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Cost with ID {cost_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_cost(cost_id: str, daily_cost: float) -> dict:
    """
    Updates a specific campaign cost in ServiceTitan Marketing API.
    
    Args:
        cost_id: The ID of the cost to update (required)
        daily_cost: New daily cost amount (required)
    
    Returns:
        dict: JSON response containing the updated cost ID
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/costs/{cost_id}"
    
    data = {"dailyCost": daily_cost}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=data)
        if response.status_code == 404:
            return {"error": f"Cost with ID {cost_id} not found"}
        if response.status_code == 400:
            return {"error": "Bad request - check cost data"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_campaigns(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    active: Optional[str] = None,  # True, Any, False
    ids: Optional[str] = None,
    name: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    campaign_phone_number: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """
    Gets a paginated list of campaigns from ServiceTitan Marketing API.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        modified_before: Return items modified before certain date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after certain date/time (RFC3339 format)
        active: What kind of items should be returned (True, Any, False) - only active items by default
        ids: Perform lookup by multiple IDs (maximum 50)
        name: Filters records by name (case-insensitive "contains" operation)
        created_before: Return items created before certain date/time (RFC3339 format)
        created_on_or_after: Return items created on or after certain date/time (RFC3339 format)
        campaign_phone_number: Filters campaigns by phone number (as string)
        sort: Applies sorting by field (+FieldName ascending, -FieldName descending).
              Available fields: Id, Name, CreatedOn, ModifiedOn
    
    Returns:
        dict: JSON response containing campaigns with fields:
              - id: Campaign ID
              - name: Campaign name
              - modifiedOn: Last modification timestamp
              - createdOn: Creation timestamp
              - active: Whether the campaign is active
              - isDefaultCampaign: Whether this is the default campaign
              - category: Campaign category details
              - source: Campaign source
              - otherSource: Other source details
              - businessUnit: Business unit name
              - medium: Campaign medium
              - otherMedium: Other medium details
              - campaignPhoneNumbers: List of phone numbers
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/campaigns"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "active": active,
        "ids": ids,
        "name": name,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "campaignPhoneNumber": campaign_phone_number,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": "Campaigns not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_campaign(
    name: str,
    business_unit_id: int,
    dnis: str,
    category_id: int,
    active: Optional[bool] = True,
    is_default_campaign: Optional[bool] = None,
    source: Optional[str] = None,
    medium: Optional[str] = None,
    other_source: Optional[str] = None,
    other_medium: Optional[str] = None
) -> dict:
    """
    Creates a new campaign in ServiceTitan Marketing API.
    
    Args:
        name: Campaign name (required)
        business_unit_id: Business unit ID (required)
        dnis: DNIS phone number (required)
        category_id: Campaign category ID (required)
        active: Whether the campaign is active
        is_default_campaign: Whether this is the default campaign
        source: Campaign source
        medium: Campaign medium
        other_source: Other source details
        other_medium: Other medium details
    
    Returns:
        dict: JSON response containing the created campaign details
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/campaigns"
    
    data = {
        "name": name,
        "businessUnitId": business_unit_id,
        "dnis": dnis,
        "categoryId": category_id,
        "active": active
    }
    
    if is_default_campaign is not None:
        data["isDefaultCampaign"] = is_default_campaign
    if source is not None:
        data["source"] = source
    if medium is not None:
        data["medium"] = medium
    if other_source is not None:
        data["otherSource"] = other_source
    if other_medium is not None:
        data["otherMedium"] = other_medium

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 400:
            return {"error": "Bad request - check campaign data"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_campaign_by_id(campaign_id: str) -> dict:
    """
    Gets a specific campaign by ID from ServiceTitan Marketing API.
    
    Args:
        campaign_id: The ID of the campaign to retrieve (required)
    
    Returns:
        dict: JSON response containing campaign details
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/campaigns/{campaign_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Campaign with ID {campaign_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_campaign(
    campaign_id: str,
    name: Optional[str] = None,
    business_unit_id: Optional[int] = None,
    dnis: Optional[str] = None,
    category_id: Optional[int] = None,
    active: Optional[bool] = None,
    is_default_campaign: Optional[bool] = None,
    source: Optional[str] = None,
    medium: Optional[str] = None,
    other_source: Optional[str] = None,
    other_medium: Optional[str] = None
) -> dict:
    """
    Updates a specific campaign in ServiceTitan Marketing API.
    
    Args:
        campaign_id: The ID of the campaign to update (required)
        name: Campaign name
        business_unit_id: Business unit ID
        dnis: DNIS phone number
        category_id: Campaign category ID
        active: Whether the campaign is active
        is_default_campaign: Whether this is the default campaign
        source: Campaign source
        medium: Campaign medium
        other_source: Other source details
        other_medium: Other medium details
    
    Returns:
        dict: JSON response containing the updated campaign details
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/campaigns/{campaign_id}"
    
    data = {}
    if name is not None:
        data["name"] = name
    if business_unit_id is not None:
        data["businessUnitId"] = business_unit_id
    if dnis is not None:
        data["dnis"] = dnis
    if category_id is not None:
        data["categoryId"] = category_id
    if active is not None:
        data["active"] = active
    if is_default_campaign is not None:
        data["isDefaultCampaign"] = is_default_campaign
    if source is not None:
        data["source"] = source
    if medium is not None:
        data["medium"] = medium
    if other_source is not None:
        data["otherSource"] = other_source
    if other_medium is not None:
        data["otherMedium"] = other_medium

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=data)
        if response.status_code == 404:
            return {"error": f"Campaign with ID {campaign_id} not found"}
        if response.status_code == 400:
            return {"error": "Bad request - check campaign data"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_campaign_costs(
    campaign_id: str,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    year: Optional[int] = None,
    month: Optional[int] = None,
    sort: Optional[str] = None
) -> dict:
    """
    Gets a paginated list of costs for a specific campaign from ServiceTitan Marketing API.
    
    Args:
        campaign_id: The ID of the campaign (required)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        year: Filter by year
        month: Filter by month
        sort: Applies sorting by field (+FieldName ascending, -FieldName descending).
              Available fields: Id, Date (Year + Month)
    
    Returns:
        dict: JSON response containing campaign costs
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/campaigns/{campaign_id}/costs"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "year": year,
        "month": month,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": f"Campaign with ID {campaign_id} not found or has no costs"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_suppressions(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    active: Optional[str] = None,  # True, Any, False
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    ids: Optional[str] = None,
    email: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """
    Gets a paginated list of email suppressions from ServiceTitan Marketing API.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        active: What kind of items should be returned (True, Any, False) - only active items by default
        modified_before: Return items modified before certain date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after certain date/time (RFC3339 format)
        created_before: Return items created before certain date/time (RFC3339 format)
        created_on_or_after: Return items created on or after certain date/time (RFC3339 format)
        ids: Perform lookup by multiple IDs (maximum 50)
        email: Filters suppressions by email
        sort: Applies sorting by field (+FieldName ascending, -FieldName descending).
              Available fields: Id, Email, CreatedOn, ModifiedOn
    
    Returns:
        dict: JSON response containing suppressions with fields:
              - id: Suppression ID
              - email: Suppressed email address
              - reason: Suppression reason
              - modifiedOn: Last modification timestamp
              - createdOn: Creation timestamp
              - active: Whether the suppression is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/suppressions"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "active": active,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "ids": ids,
        "email": email,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        if response.status_code == 404:
            return {"error": "Suppressions not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_suppression_by_email(email: str) -> dict:
    """
    Gets a specific email suppression by email address from ServiceTitan Marketing API.
    
    Args:
        email: The email address to look up (required)
    
    Returns:
        dict: JSON response containing suppression details
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/suppressions/{email}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Suppression for email {email} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def suppress_emails(emails: List[str], reason: Optional[str] = "Unsubscribe") -> dict:
    """
    Adds emails to the suppression list in ServiceTitan Marketing API.
    
    Args:
        emails: List of email addresses to suppress (required)
        reason: Reason for suppression (default: "Unsubscribe")
    
    Returns:
        dict: JSON response confirming the suppression
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/suppressions/suppress"
    
    data = {
        "emails": emails,
        "reason": reason
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 400:
            return {"error": "Bad request - check email data"}
        response.raise_for_status()
        return {"success": "Emails successfully suppressed"}

@mcp.tool()
async def unsuppress_emails(emails: List[str]) -> dict:
    """
    Removes emails from the suppression list in ServiceTitan Marketing API.
    
    Args:
        emails: List of email addresses to unsuppress (required)
    
    Returns:
        dict: JSON response confirming the unsuppression
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/suppressions/unsuppress"
    
    data = {"emails": emails}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        if response.status_code == 400:
            return {"error": "Bad request - check email data"}
        response.raise_for_status()
        return {"success": "Emails successfully unsuppressed"}

if __name__ == "__main__":
    mcp.run(transport="stdio") 