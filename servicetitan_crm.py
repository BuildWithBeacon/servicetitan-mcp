from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import httpx
from typing import Optional

# Load .env values
load_dotenv()

# Env vars
CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")

# OAuth + API URLs
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
CRM_BASE_URL = "https://api.servicetitan.io/crm/v2"

# FastMCP instance for CRM v2 API
mcp = FastMCP("servicetitan-crm")

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

# BOOKING PROVIDER TAGS ENDPOINTS

@mcp.tool()
async def get_booking_provider_tags(
    name: Optional[str] = None,
    ids: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of booking provider tags with optional filtering."""
    access_token = await get_access_token()
    
    params = {}
    if name is not None: params["name"] = name
    if ids is not None: params["ids"] = ids
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/booking-provider-tags",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_booking_provider_tag(
    tag_name: str,
    description: Optional[str] = None
) -> dict:
    """Create a booking provider tag."""
    access_token = await get_access_token()
    
    body = {"tagName": tag_name}
    if description is not None: body["description"] = description
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/booking-provider-tags",
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
async def get_booking_provider_tag_by_id(id: int) -> dict:
    """Gets a single booking provider tag by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/booking-provider-tags/{id}",
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
async def update_booking_provider_tag(
    id: int,
    tag_name: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """Update a booking provider tag."""
    access_token = await get_access_token()
    
    body = {}
    if tag_name is not None: body["tagName"] = tag_name
    if description is not None: body["description"] = description
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/booking-provider-tags/{id}",
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

# BOOKINGS ENDPOINTS

@mcp.tool()
async def get_booking_by_id(id: int) -> dict:
    """Gets a single booking by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/bookings/{id}",
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
async def get_bookings(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of bookings with optional filtering."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/bookings",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

# CONTACTS ENDPOINTS

@mcp.tool()
async def get_contact_by_id(id: int) -> dict:
    """Gets a single contact by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/contacts/{id}",
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
async def get_contacts(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of contacts with optional filtering."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/contacts",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_contact(
    name: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None
) -> dict:
    """Create a new contact."""
    access_token = await get_access_token()
    
    body = {"name": name}
    if email is not None: body["email"] = email
    if phone is not None: body["phone"] = phone
    if address is not None: body["address"] = address
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/contacts",
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
async def update_contact(
    id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None
) -> dict:
    """Update an existing contact."""
    access_token = await get_access_token()
    
    body = {}
    if name is not None: body["name"] = name
    if email is not None: body["email"] = email
    if phone is not None: body["phone"] = phone
    if address is not None: body["address"] = address
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/contacts/{id}",
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

# CUSTOMERS ENDPOINTS (Enhanced from core)

@mcp.tool()
async def get_customers(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None
) -> dict:
    """Gets a list of customers with comprehensive filtering."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None: params["sort"] = sort
    if name is not None: params["name"] = name
    if email is not None: params["email"] = email
    if phone is not None: params["phone"] = phone
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/customers",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_customer(
    name: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None,
    type: Optional[str] = None
) -> dict:
    """Create a new customer."""
    access_token = await get_access_token()
    
    body = {"name": name}
    if email is not None: body["email"] = email
    if phone is not None: body["phone"] = phone
    if address is not None: body["address"] = address
    if type is not None: body["type"] = type
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/customers",
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
async def update_customer(
    id: int,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    address: Optional[str] = None,
    type: Optional[str] = None
) -> dict:
    """Update an existing customer."""
    access_token = await get_access_token()
    
    body = {}
    if name is not None: body["name"] = name
    if email is not None: body["email"] = email
    if phone is not None: body["phone"] = phone
    if address is not None: body["address"] = address
    if type is not None: body["type"] = type
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/customers/{id}",
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

# LEADS ENDPOINTS

@mcp.tool()
async def get_lead_by_id(id: int) -> dict:
    """Gets a single lead by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/leads/{id}",
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
async def get_leads(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None,
    status: Optional[str] = None,
    source: Optional[str] = None
) -> dict:
    """Gets a list of leads with optional filtering."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None: params["sort"] = sort
    if status is not None: params["status"] = status
    if source is not None: params["source"] = source
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/leads",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_lead(
    name: str,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    source: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """Create a new lead."""
    access_token = await get_access_token()
    
    body = {"name": name}
    if phone is not None: body["phone"] = phone
    if email is not None: body["email"] = email
    if address is not None: body["address"] = address
    if source is not None: body["source"] = source
    if description is not None: body["description"] = description
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/leads",
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
async def update_lead(
    id: int,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    address: Optional[str] = None,
    source: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None
) -> dict:
    """Update an existing lead."""
    access_token = await get_access_token()
    
    body = {}
    if name is not None: body["name"] = name
    if phone is not None: body["phone"] = phone
    if email is not None: body["email"] = email
    if address is not None: body["address"] = address
    if source is not None: body["source"] = source
    if description is not None: body["description"] = description
    if status is not None: body["status"] = status
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/leads/{id}",
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

# LOCATIONS ENDPOINTS

@mcp.tool()
async def get_location_by_id(id: int) -> dict:
    """Gets a single location by ID."""
    access_token = await get_access_token()
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/locations/{id}",
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
async def get_locations(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None,
    name: Optional[str] = None,
    address: Optional[str] = None
) -> dict:
    """Gets a list of locations with optional filtering."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None: params["sort"] = sort
    if name is not None: params["name"] = name
    if address is not None: params["address"] = address
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/locations",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_location(
    name: str,
    address: str,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    phone: Optional[str] = None
) -> dict:
    """Create a new location."""
    access_token = await get_access_token()
    
    body = {"name": name, "address": address}
    if city is not None: body["city"] = city
    if state is not None: body["state"] = state
    if zip_code is not None: body["zipCode"] = zip_code
    if phone is not None: body["phone"] = phone
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/locations",
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
async def update_location(
    id: int,
    name: Optional[str] = None,
    address: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    phone: Optional[str] = None
) -> dict:
    """Update an existing location."""
    access_token = await get_access_token()
    
    body = {}
    if name is not None: body["name"] = name
    if address is not None: body["address"] = address
    if city is not None: body["city"] = city
    if state is not None: body["state"] = state
    if zip_code is not None: body["zipCode"] = zip_code
    if phone is not None: body["phone"] = phone
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/locations/{id}",
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

# TAGS ENDPOINTS

@mcp.tool()
async def get_tags(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> dict:
    """Gets a list of tags with optional filtering."""
    access_token = await get_access_token()
    
    params = {}
    if page is not None: params["page"] = page
    if page_size is not None: params["pageSize"] = page_size
    if include_total is not None: params["includeTotal"] = include_total
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort is not None: params["sort"] = sort
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/tags",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_tag(
    name: str,
    description: Optional[str] = None,
    color: Optional[str] = None
) -> dict:
    """Create a new tag."""
    access_token = await get_access_token()
    
    body = {"name": name}
    if description is not None: body["description"] = description
    if color is not None: body["color"] = color
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/tags",
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

# EXPORT ENDPOINTS

@mcp.tool()
async def export_bookings(
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None
) -> dict:
    """Export bookings data."""
    access_token = await get_access_token()
    
    params = {}
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/export/bookings",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_customers(
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None
) -> dict:
    """Export customers data."""
    access_token = await get_access_token()
    
    params = {}
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/export/customers",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_leads(
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None
) -> dict:
    """Export leads data."""
    access_token = await get_access_token()
    
    params = {}
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/export/leads",
            params=params,
            headers={
                "Authorization": f"Bearer {access_token}",
                "ST-App-Key": APP_KEY
            }
        )
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_locations(
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None
) -> dict:
    """Export locations data."""
    access_token = await get_access_token()
    
    params = {}
    if created_before is not None: params["createdBefore"] = created_before
    if created_on_or_after is not None: params["createdOnOrAfter"] = created_on_or_after
    if modified_before is not None: params["modifiedBefore"] = modified_before
    if modified_on_or_after is not None: params["modifiedOnOrAfter"] = modified_on_or_after
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CRM_BASE_URL}/tenant/{TENANT_ID}/export/locations",
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