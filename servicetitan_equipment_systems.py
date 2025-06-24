#!/usr/bin/env python3
"""
ServiceTitan Equipment Systems v2 API MCP Server

This server provides access to ServiceTitan's Equipment Systems v2 API endpoints,
focusing on installed equipment management, tracking, and maintenance.

Author: Assistant
Version: 1.0.0
"""

from mcp.server.fastmcp import FastMCP
import os
import httpx
from typing import Optional, Dict, Any, List
import time

# Configuration
CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID") 
CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")

# Validate environment variables on import
if not all([CLIENT_ID, CLIENT_SECRET, APP_KEY, TENANT_ID]):
    missing_vars = []
    if not CLIENT_ID: missing_vars.append("SERVICE_TITAN_CLIENT_ID")
    if not CLIENT_SECRET: missing_vars.append("SERVICE_TITAN_CLIENT_SECRET") 
    if not APP_KEY: missing_vars.append("SERVICE_TITAN_APP_KEY")
    if not TENANT_ID: missing_vars.append("SERVICE_TITAN_TENANT_ID")
    
    # Missing environment variables will be caught later in get_access_token()
    # Don't raise an error on import, just warn

# Base URLs
AUTH_BASE_URL = "https://auth.servicetitan.io"
API_BASE_URL = "https://api.servicetitan.io/equipmentsystems/v2"

# Global variables for token management
_access_token = None
_token_expires_at = 0

mcp = FastMCP("servicetitan-equipment-systems")

async def get_access_token() -> str:
    """Get a valid access token, refreshing if necessary."""
    global _access_token, _token_expires_at
    
    if not all([CLIENT_ID, CLIENT_SECRET, APP_KEY, TENANT_ID]):
        missing_vars = []
        if not CLIENT_ID: missing_vars.append("SERVICE_TITAN_CLIENT_ID")
        if not CLIENT_SECRET: missing_vars.append("SERVICE_TITAN_CLIENT_SECRET") 
        if not APP_KEY: missing_vars.append("SERVICE_TITAN_APP_KEY")
        if not TENANT_ID: missing_vars.append("SERVICE_TITAN_TENANT_ID")
        error_msg = f"ERROR_ENV: Missing ServiceTitan environment variables: {', '.join(missing_vars)}"
        raise ValueError(error_msg)
    
    if _access_token and time.time() < _token_expires_at:
        return _access_token
    
    async with httpx.AsyncClient() as client:
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        
        response = await client.post(f"{AUTH_BASE_URL}/connect/token", data=auth_data)
        if response.status_code != 200:
            raise Exception(f"Failed to get access token: {response.status_code}")
        
        token_data = response.json()
        _access_token = token_data["access_token"]
        _token_expires_at = time.time() + token_data["expires_in"] - 60  # 60 second buffer
        
        return _access_token

async def make_api_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make an authenticated API request to ServiceTitan."""
    token = await get_access_token()
    
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{API_BASE_URL}/tenant/{TENANT_ID}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers, params=params, json=data)
        if response.status_code >= 400:
            error_text = response.text
            raise Exception(f"API request failed: {response.status_code} - {error_text}")
        
        return response.json()

# INSTALLED EQUIPMENT MANAGEMENT
@mcp.tool()
async def get_installed_equipment(
    location_ids: Optional[str] = None,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None,
    active: Optional[str] = "True"
) -> Dict[str, Any]:
    """
    Retrieve a list of installed equipment with comprehensive filtering options.
    
    Args:
        location_ids: Comma-delimited list of location IDs to filter by
        ids: Perform lookup by multiple IDs (maximum 50)
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Applies sorting by specified field (+FieldName for ascending, -FieldName for descending)
               Available fields: Id, CreatedOn, ModifiedOn
        active: What kind of items should be returned (True, Any, False)
    
    Returns:
        Dictionary containing installed equipment data
    """
    params = {}
    if location_ids: params["locationIds"] = location_ids
    if ids: params["ids"] = ids
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if sort: params["sort"] = sort
    if active: params["active"] = active
    
    return await make_api_request("GET", "/installed-equipment", params=params)

@mcp.tool()
async def get_installed_equipment_by_id(equipment_id: int) -> Dict[str, Any]:
    """
    Retrieve a specific installed equipment item by its ID.
    
    Args:
        equipment_id: The ID of the installed equipment to retrieve
    
    Returns:
        Dictionary containing the installed equipment details
    """
    return await make_api_request("GET", f"/installed-equipment/{equipment_id}")

@mcp.tool()
async def create_installed_equipment(
    location_id: int,
    name: str,
    installed_on: Optional[str] = None,
    actual_replacement_date: Optional[str] = None,
    serial_number: Optional[str] = None,
    barcode_id: Optional[str] = None,
    memo: Optional[str] = None,
    manufacturer: Optional[str] = None,
    model: Optional[str] = None,
    cost: Optional[float] = None,
    manufacturer_warranty_start: Optional[str] = None,
    manufacturer_warranty_end: Optional[str] = None,
    service_provider_warranty_start: Optional[str] = None,
    service_provider_warranty_end: Optional[str] = None,
    custom_fields: Optional[List[Dict[str, Any]]] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
    tag_type_ids: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    Create a new installed equipment record.
    
    Args:
        location_id: The location where the equipment is installed
        name: Name/description of the equipment
        installed_on: Date when the equipment was installed
        actual_replacement_date: Date when equipment was actually replaced
        serial_number: Equipment serial number
        barcode_id: Barcode identifier for the equipment
        memo: Additional notes about the equipment
        manufacturer: Equipment manufacturer
        model: Equipment model
        cost: Cost of the equipment
        manufacturer_warranty_start: Start date of manufacturer warranty
        manufacturer_warranty_end: End date of manufacturer warranty
        service_provider_warranty_start: Start date of service provider warranty
        service_provider_warranty_end: End date of service provider warranty
        custom_fields: List of custom field objects with id, typeId, and value
        attachments: List of attachment objects with alias, fileName, type, and url
        tag_type_ids: List of tag type IDs to associate with the equipment
    
    Returns:
        Dictionary containing the created installed equipment data
    """
    data = {
        "locationId": location_id,
        "name": name
    }
    
    if installed_on is not None: data["installedOn"] = installed_on
    if actual_replacement_date is not None: data["actualReplacementDate"] = actual_replacement_date
    if serial_number is not None: data["serialNumber"] = serial_number
    if barcode_id is not None: data["barcodeId"] = barcode_id
    if memo is not None: data["memo"] = memo
    if manufacturer is not None: data["manufacturer"] = manufacturer
    if model is not None: data["model"] = model
    if cost is not None: data["cost"] = cost
    if manufacturer_warranty_start is not None: data["manufacturerWarrantyStart"] = manufacturer_warranty_start
    if manufacturer_warranty_end is not None: data["manufacturerWarrantyEnd"] = manufacturer_warranty_end
    if service_provider_warranty_start is not None: data["serviceProviderWarrantyStart"] = service_provider_warranty_start
    if service_provider_warranty_end is not None: data["serviceProviderWarrantyEnd"] = service_provider_warranty_end
    if custom_fields is not None: data["customFields"] = custom_fields
    if attachments is not None: data["attachments"] = attachments
    if tag_type_ids is not None: data["tagTypeIds"] = tag_type_ids
    
    return await make_api_request("POST", "/installed-equipment", data=data)

@mcp.tool()
async def update_installed_equipment(
    equipment_id: int,
    name: Optional[str] = None,
    installed_on: Optional[str] = None,
    actual_replacement_date: Optional[str] = None,
    serial_number: Optional[str] = None,
    barcode_id: Optional[str] = None,
    memo: Optional[str] = None,
    manufacturer: Optional[str] = None,
    model: Optional[str] = None,
    cost: Optional[float] = None,
    manufacturer_warranty_start: Optional[str] = None,
    manufacturer_warranty_end: Optional[str] = None,
    service_provider_warranty_start: Optional[str] = None,
    service_provider_warranty_end: Optional[str] = None,
    custom_fields: Optional[List[Dict[str, Any]]] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
    tag_type_ids: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    Update an existing installed equipment record.
    
    Args:
        equipment_id: The ID of the installed equipment to update
        name: Name/description of the equipment
        installed_on: Date when the equipment was installed
        actual_replacement_date: Date when equipment was actually replaced
        serial_number: Equipment serial number
        barcode_id: Barcode identifier for the equipment
        memo: Additional notes about the equipment
        manufacturer: Equipment manufacturer
        model: Equipment model
        cost: Cost of the equipment
        manufacturer_warranty_start: Start date of manufacturer warranty
        manufacturer_warranty_end: End date of manufacturer warranty
        service_provider_warranty_start: Start date of service provider warranty
        service_provider_warranty_end: End date of service provider warranty
        custom_fields: List of custom field objects with id, typeId, and value
        attachments: List of attachment objects with alias, fileName, type, and url
        tag_type_ids: List of tag type IDs to associate with the equipment
    
    Returns:
        Dictionary containing the updated installed equipment data
    """
    data = {}
    
    if name is not None: data["name"] = name
    if installed_on is not None: data["installedOn"] = installed_on
    if actual_replacement_date is not None: data["actualReplacementDate"] = actual_replacement_date
    if serial_number is not None: data["serialNumber"] = serial_number
    if barcode_id is not None: data["barcodeId"] = barcode_id
    if memo is not None: data["memo"] = memo
    if manufacturer is not None: data["manufacturer"] = manufacturer
    if model is not None: data["model"] = model
    if cost is not None: data["cost"] = cost
    if manufacturer_warranty_start is not None: data["manufacturerWarrantyStart"] = manufacturer_warranty_start
    if manufacturer_warranty_end is not None: data["manufacturerWarrantyEnd"] = manufacturer_warranty_end
    if service_provider_warranty_start is not None: data["serviceProviderWarrantyStart"] = service_provider_warranty_start
    if service_provider_warranty_end is not None: data["serviceProviderWarrantyEnd"] = service_provider_warranty_end
    if custom_fields is not None: data["customFields"] = custom_fields
    if attachments is not None: data["attachments"] = attachments
    if tag_type_ids is not None: data["tagTypeIds"] = tag_type_ids
    
    return await make_api_request("PATCH", f"/installed-equipment/{equipment_id}", data=data)

# EQUIPMENT EXPORT
@mcp.tool()
async def export_installed_equipment(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Export installed equipment data for external systems integration.
    
    Args:
        from_token: Continuation token from previous export or custom date (e.g., "2020-01-01")
        include_recent_changes: Use "true" to receive most recent changes quicker
    
    Returns:
        Dictionary containing export data with continuation token
    """
    params = {}
    if from_token: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    return await make_api_request("GET", "/export/installed-equipment", params=params)

# ATTACHMENT MANAGEMENT
@mcp.tool()
async def upload_equipment_attachment(file_content: str) -> Dict[str, Any]:
    """
    Upload an attachment file for installed equipment.
    
    Args:
        file_content: Base64 encoded file content
    
    Returns:
        Dictionary containing the uploaded file path
    """
    data = {"file": file_content}
    return await make_api_request("POST", "/installed-equipment/attachments", data=data)

@mcp.tool()
async def get_equipment_attachment(path: str) -> Dict[str, Any]:
    """
    Retrieve an equipment attachment by its path.
    
    Args:
        path: The path of the attachment to retrieve
    
    Returns:
        Dictionary containing attachment data or redirect information
    """
    params = {"path": path}
    return await make_api_request("GET", "/installed-equipment/attachments", params=params)

# EQUIPMENT SEARCH AND FILTERING HELPERS
@mcp.tool()
async def search_equipment_by_location(
    location_id: int,
    active_only: bool = True,
    include_warranty_info: bool = True
) -> Dict[str, Any]:
    """
    Search for all equipment installed at a specific location.
    
    Args:
        location_id: The location ID to search for equipment
        active_only: Whether to return only active equipment (default: True)
        include_warranty_info: Whether to include warranty information
    
    Returns:
        Dictionary containing equipment at the specified location
    """
    active_filter = "True" if active_only else "Any"
    return await get_installed_equipment(
        location_ids=str(location_id),
        active=active_filter,
        page_size=100  # Get more results for location searches
    )

@mcp.tool()
async def search_equipment_by_manufacturer(
    manufacturer: str,
    active_only: bool = True
) -> Dict[str, Any]:
    """
    Search for equipment by manufacturer. Note: This requires fetching and filtering client-side.
    
    Args:
        manufacturer: Manufacturer name to search for
        active_only: Whether to return only active equipment
    
    Returns:
        Dictionary containing equipment from the specified manufacturer
    """
    # Note: The API doesn't support direct manufacturer filtering, so we need to fetch and filter
    active_filter = "True" if active_only else "Any"
    all_equipment = await get_installed_equipment(active=active_filter, page_size=100)
    
    # Filter by manufacturer client-side
    if "data" in all_equipment:
        filtered_data = [
            item for item in all_equipment["data"]
            if item.get("manufacturer", "").lower() == manufacturer.lower()
        ]
        all_equipment["data"] = filtered_data
        all_equipment["filteredBy"] = f"manufacturer={manufacturer}"
    
    return all_equipment

@mcp.tool()
async def search_equipment_by_serial_number(
    serial_number: str,
    active_only: bool = True
) -> Dict[str, Any]:
    """
    Search for equipment by serial number. Note: This requires fetching and filtering client-side.
    
    Args:
        serial_number: Serial number to search for
        active_only: Whether to return only active equipment
    
    Returns:
        Dictionary containing equipment with the specified serial number
    """
    active_filter = "True" if active_only else "Any"
    all_equipment = await get_installed_equipment(active=active_filter, page_size=100)
    
    # Filter by serial number client-side
    if "data" in all_equipment:
        filtered_data = [
            item for item in all_equipment["data"]
            if item.get("serialNumber", "").lower() == serial_number.lower()
        ]
        all_equipment["data"] = filtered_data
        all_equipment["filteredBy"] = f"serialNumber={serial_number}"
    
    return all_equipment

@mcp.tool()
async def get_equipment_warranty_status(equipment_id: int) -> Dict[str, Any]:
    """
    Get warranty status information for a specific piece of equipment.
    
    Args:
        equipment_id: The ID of the equipment to check warranty status
    
    Returns:
        Dictionary containing warranty status and dates
    """
    equipment = await get_installed_equipment_by_id(equipment_id)
    
    import datetime
    current_date = datetime.datetime.now().isoformat()
    
    warranty_status = {
        "equipmentId": equipment_id,
        "currentDate": current_date,
        "manufacturerWarranty": {
            "start": equipment.get("manufacturerWarrantyStart"),
            "end": equipment.get("manufacturerWarrantyEnd"),
            "active": False
        },
        "serviceProviderWarranty": {
            "start": equipment.get("serviceProviderWarrantyStart"),
            "end": equipment.get("serviceProviderWarrantyEnd"),
            "active": False
        }
    }
    
    # Check if warranties are currently active
    try:
        if equipment.get("manufacturerWarrantyStart") and equipment.get("manufacturerWarrantyEnd"):
            start_date = datetime.datetime.fromisoformat(equipment["manufacturerWarrantyStart"].replace("Z", "+00:00"))
            end_date = datetime.datetime.fromisoformat(equipment["manufacturerWarrantyEnd"].replace("Z", "+00:00"))
            now = datetime.datetime.now(datetime.timezone.utc)
            warranty_status["manufacturerWarranty"]["active"] = start_date <= now <= end_date
            
        if equipment.get("serviceProviderWarrantyStart") and equipment.get("serviceProviderWarrantyEnd"):
            start_date = datetime.datetime.fromisoformat(equipment["serviceProviderWarrantyStart"].replace("Z", "+00:00"))
            end_date = datetime.datetime.fromisoformat(equipment["serviceProviderWarrantyEnd"].replace("Z", "+00:00"))
            now = datetime.datetime.now(datetime.timezone.utc)
            warranty_status["serviceProviderWarranty"]["active"] = start_date <= now <= end_date
    except:
        # If date parsing fails, leave active status as False
        pass
    
    return warranty_status

@mcp.tool()
async def get_equipment_replacement_predictions(
    location_id: Optional[int] = None,
    months_ahead: int = 12
) -> Dict[str, Any]:
    """
    Get equipment replacement predictions for planning purposes.
    
    Args:
        location_id: Optional location ID to filter by
        months_ahead: Number of months ahead to look for replacements (default: 12)
    
    Returns:
        Dictionary containing equipment that may need replacement
    """
    params = {}
    if location_id:
        params["location_ids"] = str(location_id)
    
    equipment_list = await get_installed_equipment(**params, page_size=100)
    
    import datetime
    current_date = datetime.datetime.now()
    future_date = current_date + datetime.timedelta(days=months_ahead * 30)  # Approximate months
    
    replacement_candidates = []
    
    if "data" in equipment_list:
        for item in equipment_list["data"]:
            predicted_date = item.get("predictedReplacementDate")
            if predicted_date:
                try:
                    pred_date = datetime.datetime.fromisoformat(predicted_date.replace("Z", "+00:00"))
                    if current_date <= pred_date <= future_date:
                        replacement_candidates.append({
                            "equipment": item,
                            "predictedReplacementDate": predicted_date,
                            "monthsUntilReplacement": item.get("predictedReplacementMonths", 0)
                        })
                except:
                    # Skip items with invalid dates
                    continue
    
    return {
        "searchCriteria": {
            "locationId": location_id,
            "monthsAhead": months_ahead,
            "searchDate": current_date.isoformat()
        },
        "replacementCandidates": replacement_candidates,
        "totalCount": len(replacement_candidates)
    }

if __name__ == "__main__":
    mcp.run(transport="stdio") 