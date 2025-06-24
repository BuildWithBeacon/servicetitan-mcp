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

# FastMCP instance for Inventory v2 API
mcp = FastMCP("servicetitan-inventory")

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

# BASE URL: https://api.servicetitan.io/inventory/v2

# ADJUSTMENTS ENDPOINTS

@mcp.tool()
async def get_inventory_adjustments(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    number: Optional[str] = None,
    reference_number: Optional[str] = None,
    batch_id: Optional[int] = None,
    invoice_ids: Optional[str] = None,
    inventory_location_ids: Optional[str] = None,
    adjustment_types: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    sync_statuses: Optional[str] = None,
    custom_fields_fields: Optional[dict] = None,
    custom_fields_operator: Optional[str] = None,
    date_on_or_after: Optional[str] = None,
    date_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of inventory adjustments from ServiceTitan.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        active: What kind of items should be returned ("True", "Any", "False")
        external_data_application_guid: GUID for external data filtering
        external_data_key: External data key for lookup
        external_data_values: External data values for lookup (max 50)
        number: Number filter
        reference_number: Reference number filter
        batch_id: BatchId filter
        invoice_ids: Filter by collection of invoice IDs
        inventory_location_ids: Filter by collection of inventory location IDs
        adjustment_types: Filter by collection of adjustment types
        business_unit_ids: Filter by collection of business unit IDs
        sync_statuses: Filter by collection of sync statuses
        custom_fields_fields: Collection of custom field pairs (name, value)
        custom_fields_operator: Custom fields operator ("And" or "Or")
        date_on_or_after: Return adjustments with date on or after (RFC3339)
        date_before: Return adjustments with date before (RFC3339)
        created_on_or_after: Return items created on or after (RFC3339)
        created_before: Return items created before (RFC3339)
        modified_on_or_after: Return items modified on or after (RFC3339)
        modified_before: Return items modified before (RFC3339)
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName ascending, -FieldName descending)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/adjustments"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "number": number,
        "referenceNumber": reference_number,
        "batchId": batch_id,
        "invoiceIds": invoice_ids,
        "inventoryLocationIds": inventory_location_ids,
        "adjustmentTypes": adjustment_types,
        "businessUnitIds": business_unit_ids,
        "syncStatuses": sync_statuses,
        "customFields.Fields": custom_fields_fields,
        "customFields.Operator": custom_fields_operator,
        "dateOnOrAfter": date_on_or_after,
        "dateBefore": date_before,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_adjustment(
    adjustment_id: str,
    external_data: Optional[dict] = None
) -> dict:
    """
    Update an existing inventory adjustment.
    
    Args:
        adjustment_id: ID of the adjustment to update (required)
        external_data: External data update model with patchMode, applicationGuid, and externalData
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/adjustments/{adjustment_id}"

    request_body = {}
    if external_data is not None:
        request_body["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Adjustment {adjustment_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_adjustment_custom_fields(
    custom_fields: list
) -> dict:
    """
    Update custom fields for inventory adjustments.
    
    Args:
        custom_fields: List of custom field updates (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/adjustments/custom-fields"

    request_body = {"customFields": custom_fields}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

# PURCHASE ORDERS ENDPOINTS

@mcp.tool()
async def create_purchase_order(
    purchase_order_type_id: int,
    business_unit_id: int,
    inventory_location_id: int,
    vendor_id: int,
    items: list,
    reference_number: Optional[str] = None,
    memo: Optional[str] = None,
    shipment_date: Optional[str] = None,
    needed_date: Optional[str] = None,
    requestor_id: Optional[int] = None,
    external_data: Optional[dict] = None,
    custom_fields: Optional[list] = None
) -> dict:
    """
    Create a new purchase order in ServiceTitan inventory.
    
    Args:
        purchase_order_type_id: ID of purchase order type (required)
        business_unit_id: ID of business unit (required)
        inventory_location_id: ID of inventory location (required)
        vendor_id: ID of vendor (required)
        items: List of items for the purchase order (required)
        reference_number: Reference number for the purchase order
        memo: Memo/notes for the purchase order
        shipment_date: Expected shipment date (RFC3339)
        needed_date: Date when items are needed (RFC3339)
        requestor_id: ID of the requestor
        external_data: External data to attach
        custom_fields: Custom fields for the purchase order
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-orders"

    request_body = {
        "purchaseOrderTypeId": purchase_order_type_id,
        "businessUnitId": business_unit_id,
        "inventoryLocationId": inventory_location_id,
        "vendorId": vendor_id,
        "items": items
    }

    if reference_number is not None:
        request_body["referenceNumber"] = reference_number
    if memo is not None:
        request_body["memo"] = memo
    if shipment_date is not None:
        request_body["shipmentDate"] = shipment_date
    if needed_date is not None:
        request_body["neededDate"] = needed_date
    if requestor_id is not None:
        request_body["requestorId"] = requestor_id
    if external_data is not None:
        request_body["externalData"] = external_data
    if custom_fields is not None:
        request_body["customFields"] = custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_purchase_orders(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    number: Optional[str] = None,
    reference_number: Optional[str] = None,
    batch_id: Optional[int] = None,
    purchase_order_type_ids: Optional[str] = None,
    inventory_location_ids: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    vendor_ids: Optional[str] = None,
    sync_statuses: Optional[str] = None,
    statuses: Optional[str] = None,
    requestor_ids: Optional[str] = None,
    custom_fields_fields: Optional[dict] = None,
    custom_fields_operator: Optional[str] = None,
    date_on_or_after: Optional[str] = None,
    date_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of purchase orders from ServiceTitan inventory.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        active: What kind of items should be returned ("True", "Any", "False")
        external_data_application_guid: GUID for external data filtering
        external_data_key: External data key for lookup
        external_data_values: External data values for lookup (max 50)
        number: Number filter
        reference_number: Reference number filter
        batch_id: BatchId filter
        purchase_order_type_ids: Filter by collection of PO type IDs
        inventory_location_ids: Filter by collection of inventory location IDs
        business_unit_ids: Filter by collection of business unit IDs
        vendor_ids: Filter by collection of vendor IDs
        sync_statuses: Filter by collection of sync statuses
        statuses: Filter by collection of statuses
        requestor_ids: Filter by collection of requestor IDs
        custom_fields_fields: Collection of custom field pairs (name, value)
        custom_fields_operator: Custom fields operator ("And" or "Or")
        date_on_or_after: Return POs with date on or after (RFC3339)
        date_before: Return POs with date before (RFC3339)
        created_on_or_after: Return items created on or after (RFC3339)
        created_before: Return items created before (RFC3339)
        modified_on_or_after: Return items modified on or after (RFC3339)
        modified_before: Return items modified before (RFC3339)
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName ascending, -FieldName descending)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-orders"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "number": number,
        "referenceNumber": reference_number,
        "batchId": batch_id,
        "purchaseOrderTypeIds": purchase_order_type_ids,
        "inventoryLocationIds": inventory_location_ids,
        "businessUnitIds": business_unit_ids,
        "vendorIds": vendor_ids,
        "syncStatuses": sync_statuses,
        "statuses": statuses,
        "requestorIds": requestor_ids,
        "customFields.Fields": custom_fields_fields,
        "customFields.Operator": custom_fields_operator,
        "dateOnOrAfter": date_on_or_after,
        "dateBefore": date_before,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_purchase_order_requests(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    number: Optional[str] = None,
    reference_number: Optional[str] = None,
    batch_id: Optional[int] = None,
    purchase_order_type_ids: Optional[str] = None,
    inventory_location_ids: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    vendor_ids: Optional[str] = None,
    sync_statuses: Optional[str] = None,
    statuses: Optional[str] = None,
    requestor_ids: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of purchase order requests from ServiceTitan inventory.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-orders/requests"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "number": number,
        "referenceNumber": reference_number,
        "batchId": batch_id,
        "purchaseOrderTypeIds": purchase_order_type_ids,
        "inventoryLocationIds": inventory_location_ids,
        "businessUnitIds": business_unit_ids,
        "vendorIds": vendor_ids,
        "syncStatuses": sync_statuses,
        "statuses": statuses,
        "requestorIds": requestor_ids,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_purchase_order_by_id(
    purchase_order_id: str,
    external_data_application_guid: Optional[str] = None
) -> dict:
    """
    Get a specific purchase order by ID.
    
    Args:
        purchase_order_id: ID of the purchase order (required)
        external_data_application_guid: GUID for external data filtering
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-orders/{purchase_order_id}"

    params = {}
    if external_data_application_guid is not None:
        params["externalDataApplicationGuid"] = external_data_application_guid

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return {"error": f"Purchase order {purchase_order_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_purchase_order(
    purchase_order_id: str,
    reference_number: Optional[str] = None,
    memo: Optional[str] = None,
    shipment_date: Optional[str] = None,
    needed_date: Optional[str] = None,
    requestor_id: Optional[int] = None,
    external_data: Optional[dict] = None,
    custom_fields: Optional[list] = None
) -> dict:
    """
    Update an existing purchase order.
    
    Args:
        purchase_order_id: ID of the purchase order to update (required)
        reference_number: Reference number for the purchase order
        memo: Memo/notes for the purchase order
        shipment_date: Expected shipment date (RFC3339)
        needed_date: Date when items are needed (RFC3339)
        requestor_id: ID of the requestor
        external_data: External data update model
        custom_fields: Custom fields for the purchase order
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-orders/{purchase_order_id}"

    request_body = {}

    if reference_number is not None:
        request_body["referenceNumber"] = reference_number
    if memo is not None:
        request_body["memo"] = memo
    if shipment_date is not None:
        request_body["shipmentDate"] = shipment_date
    if needed_date is not None:
        request_body["neededDate"] = needed_date
    if requestor_id is not None:
        request_body["requestorId"] = requestor_id
    if external_data is not None:
        request_body["externalData"] = external_data
    if custom_fields is not None:
        request_body["customFields"] = custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Purchase order {purchase_order_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def cancel_purchase_order(
    purchase_order_id: str,
    reason: str
) -> dict:
    """
    Cancel a purchase order.
    
    Args:
        purchase_order_id: ID of the purchase order to cancel (required)
        reason: Reason for cancellation (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-orders/{purchase_order_id}/cancellation"

    request_body = {"reason": reason}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Purchase order {purchase_order_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def approve_purchase_order_request(
    request_id: str,
    approver_notes: Optional[str] = None
) -> dict:
    """
    Approve a purchase order request.
    
    Args:
        request_id: ID of the purchase order request to approve (required)
        approver_notes: Notes from the approver
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-orders/requests/{request_id}/approve"

    request_body = {}
    if approver_notes is not None:
        request_body["approverNotes"] = approver_notes

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Purchase order request {request_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def reject_purchase_order_request(
    request_id: str,
    reason: str,
    approver_notes: Optional[str] = None
) -> dict:
    """
    Reject a purchase order request.
    
    Args:
        request_id: ID of the purchase order request to reject (required)
        reason: Reason for rejection (required)
        approver_notes: Notes from the approver
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-orders/requests/{request_id}/reject"

    request_body = {"reason": reason}
    if approver_notes is not None:
        request_body["approverNotes"] = approver_notes

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Purchase order request {request_id} not found"}
        response.raise_for_status()
        return response.json()

# PURCHASE ORDER MARKUPS ENDPOINTS

@mcp.tool()
async def get_purchase_order_markups(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Get purchase order markup configurations.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-order-markups"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_purchase_order_markup(
    name: str,
    markup_percentage: float,
    active: Optional[bool] = True
) -> dict:
    """
    Create a new purchase order markup configuration.
    
    Args:
        name: Name of the markup configuration (required)
        markup_percentage: Markup percentage (required)
        active: Whether the markup is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-order-markups"

    request_body = {
        "name": name,
        "markupPercentage": markup_percentage
    }

    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_purchase_order_markup_by_id(markup_id: str) -> dict:
    """
    Get a specific purchase order markup by ID.
    
    Args:
        markup_id: ID of the markup configuration (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-order-markups/{markup_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Purchase order markup {markup_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_purchase_order_markup(
    markup_id: str,
    name: Optional[str] = None,
    markup_percentage: Optional[float] = None,
    active: Optional[bool] = None
) -> dict:
    """
    Update an existing purchase order markup configuration.
    
    Args:
        markup_id: ID of the markup configuration to update (required)
        name: Name of the markup configuration
        markup_percentage: Markup percentage
        active: Whether the markup is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-order-markups/{markup_id}"

    request_body = {}

    if name is not None:
        request_body["name"] = name
    if markup_percentage is not None:
        request_body["markupPercentage"] = markup_percentage
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Purchase order markup {markup_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_purchase_order_markup(markup_id: str) -> dict:
    """
    Delete a purchase order markup configuration.
    
    Args:
        markup_id: ID of the markup configuration to delete (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-order-markups/{markup_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Purchase order markup {markup_id} not found"}
        response.raise_for_status()
        return {"success": f"Purchase order markup {markup_id} deleted successfully"}

# PURCHASE ORDER TYPES ENDPOINTS

@mcp.tool()
async def create_purchase_order_type(
    name: str,
    description: Optional[str] = None,
    active: Optional[bool] = True
) -> dict:
    """
    Create a new purchase order type.
    
    Args:
        name: Name of the purchase order type (required)
        description: Description of the purchase order type
        active: Whether the type is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-order-types"

    request_body = {"name": name}

    if description is not None:
        request_body["description"] = description
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_purchase_order_types(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Get purchase order types.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-order-types"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_purchase_order_type(
    type_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    active: Optional[bool] = None
) -> dict:
    """
    Update an existing purchase order type.
    
    Args:
        type_id: ID of the purchase order type to update (required)
        name: Name of the purchase order type
        description: Description of the purchase order type
        active: Whether the type is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/purchase-order-types/{type_id}"

    request_body = {}

    if name is not None:
        request_body["name"] = name
    if description is not None:
        request_body["description"] = description
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Purchase order type {type_id} not found"}
        response.raise_for_status()
        return response.json()

# RECEIPTS ENDPOINTS

@mcp.tool()
async def get_inventory_receipts(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    number: Optional[str] = None,
    reference_number: Optional[str] = None,
    batch_id: Optional[int] = None,
    purchase_order_ids: Optional[str] = None,
    inventory_location_ids: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    vendor_ids: Optional[str] = None,
    sync_statuses: Optional[str] = None,
    custom_fields_fields: Optional[dict] = None,
    custom_fields_operator: Optional[str] = None,
    date_on_or_after: Optional[str] = None,
    date_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of inventory receipts from ServiceTitan.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/receipts"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "number": number,
        "referenceNumber": reference_number,
        "batchId": batch_id,
        "purchaseOrderIds": purchase_order_ids,
        "inventoryLocationIds": inventory_location_ids,
        "businessUnitIds": business_unit_ids,
        "vendorIds": vendor_ids,
        "syncStatuses": sync_statuses,
        "customFields.Fields": custom_fields_fields,
        "customFields.Operator": custom_fields_operator,
        "dateOnOrAfter": date_on_or_after,
        "dateBefore": date_before,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_inventory_receipt(
    business_unit_id: int,
    inventory_location_id: int,
    vendor_id: int,
    items: list,
    reference_number: Optional[str] = None,
    memo: Optional[str] = None,
    date: Optional[str] = None,
    purchase_order_id: Optional[int] = None,
    external_data: Optional[dict] = None,
    custom_fields: Optional[list] = None
) -> dict:
    """
    Create a new inventory receipt.
    
    Args:
        business_unit_id: ID of business unit (required)
        inventory_location_id: ID of inventory location (required)
        vendor_id: ID of vendor (required)
        items: List of items for the receipt (required)
        reference_number: Reference number for the receipt
        memo: Memo/notes for the receipt
        date: Date of the receipt (RFC3339)
        purchase_order_id: ID of related purchase order
        external_data: External data to attach
        custom_fields: Custom fields for the receipt
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/receipts"

    request_body = {
        "businessUnitId": business_unit_id,
        "inventoryLocationId": inventory_location_id,
        "vendorId": vendor_id,
        "items": items
    }

    if reference_number is not None:
        request_body["referenceNumber"] = reference_number
    if memo is not None:
        request_body["memo"] = memo
    if date is not None:
        request_body["date"] = date
    if purchase_order_id is not None:
        request_body["purchaseOrderId"] = purchase_order_id
    if external_data is not None:
        request_body["externalData"] = external_data
    if custom_fields is not None:
        request_body["customFields"] = custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_receipt_custom_fields(
    custom_fields: list
) -> dict:
    """
    Update custom fields for inventory receipts.
    
    Args:
        custom_fields: List of custom field updates (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/receipts/custom-fields"

    request_body = {"customFields": custom_fields}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def cancel_inventory_receipt(
    receipt_id: str,
    reason: str
) -> dict:
    """
    Cancel an inventory receipt.
    
    Args:
        receipt_id: ID of the receipt to cancel (required)
        reason: Reason for cancellation (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/receipts/{receipt_id}/cancellation"

    request_body = {"reason": reason}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Receipt {receipt_id} not found"}
        response.raise_for_status()
        return response.json()

# RETURNS ENDPOINTS

@mcp.tool()
async def get_inventory_returns(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    number: Optional[str] = None,
    reference_number: Optional[str] = None,
    batch_id: Optional[int] = None,
    return_type_ids: Optional[str] = None,
    inventory_location_ids: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    vendor_ids: Optional[str] = None,
    sync_statuses: Optional[str] = None,
    custom_fields_fields: Optional[dict] = None,
    custom_fields_operator: Optional[str] = None,
    date_on_or_after: Optional[str] = None,
    date_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of inventory returns from ServiceTitan.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/returns"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "number": number,
        "referenceNumber": reference_number,
        "batchId": batch_id,
        "returnTypeIds": return_type_ids,
        "inventoryLocationIds": inventory_location_ids,
        "businessUnitIds": business_unit_ids,
        "vendorIds": vendor_ids,
        "syncStatuses": sync_statuses,
        "customFields.Fields": custom_fields_fields,
        "customFields.Operator": custom_fields_operator,
        "dateOnOrAfter": date_on_or_after,
        "dateBefore": date_before,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_inventory_return(
    return_type_id: int,
    business_unit_id: int,
    inventory_location_id: int,
    vendor_id: int,
    items: list,
    reference_number: Optional[str] = None,
    memo: Optional[str] = None,
    date: Optional[str] = None,
    external_data: Optional[dict] = None,
    custom_fields: Optional[list] = None
) -> dict:
    """
    Create a new inventory return.
    
    Args:
        return_type_id: ID of return type (required)
        business_unit_id: ID of business unit (required)
        inventory_location_id: ID of inventory location (required)
        vendor_id: ID of vendor (required)
        items: List of items for the return (required)
        reference_number: Reference number for the return
        memo: Memo/notes for the return
        date: Date of the return (RFC3339)
        external_data: External data to attach
        custom_fields: Custom fields for the return
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/returns"

    request_body = {
        "returnTypeId": return_type_id,
        "businessUnitId": business_unit_id,
        "inventoryLocationId": inventory_location_id,
        "vendorId": vendor_id,
        "items": items
    }

    if reference_number is not None:
        request_body["referenceNumber"] = reference_number
    if memo is not None:
        request_body["memo"] = memo
    if date is not None:
        request_body["date"] = date
    if external_data is not None:
        request_body["externalData"] = external_data
    if custom_fields is not None:
        request_body["customFields"] = custom_fields

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_return_custom_fields(
    custom_fields: list
) -> dict:
    """
    Update custom fields for inventory returns.
    
    Args:
        custom_fields: List of custom field updates (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/returns/custom-fields"

    request_body = {"customFields": custom_fields}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_return(
    return_id: str,
    external_data: Optional[dict] = None
) -> dict:
    """
    Update an existing inventory return.
    
    Args:
        return_id: ID of the return to update (required)
        external_data: External data update model
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/returns/{return_id}"

    request_body = {}
    if external_data is not None:
        request_body["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Return {return_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def cancel_inventory_return(
    return_id: str,
    reason: str
) -> dict:
    """
    Cancel an inventory return.
    
    Args:
        return_id: ID of the return to cancel (required)
        reason: Reason for cancellation (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/returns/{return_id}/cancellation"

    request_body = {"reason": reason}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Return {return_id} not found"}
        response.raise_for_status()
        return response.json()

# RETURN TYPES ENDPOINTS

@mcp.tool()
async def create_return_type(
    name: str,
    description: Optional[str] = None,
    active: Optional[bool] = True
) -> dict:
    """
    Create a new return type.
    
    Args:
        name: Name of the return type (required)
        description: Description of the return type
        active: Whether the type is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/return-types"

    request_body = {"name": name}

    if description is not None:
        request_body["description"] = description
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_return_types(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Get return types.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/return-types"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_return_type(
    type_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    active: Optional[bool] = None
) -> dict:
    """
    Update an existing return type.
    
    Args:
        type_id: ID of the return type to update (required)
        name: Name of the return type
        description: Description of the return type
        active: Whether the type is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/return-types/{type_id}"

    request_body = {}

    if name is not None:
        request_body["name"] = name
    if description is not None:
        request_body["description"] = description
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Return type {type_id} not found"}
        response.raise_for_status()
        return response.json()

# TRANSFERS ENDPOINTS

@mcp.tool()
async def get_inventory_transfers(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    number: Optional[str] = None,
    reference_number: Optional[str] = None,
    batch_id: Optional[int] = None,
    from_inventory_location_ids: Optional[str] = None,
    to_inventory_location_ids: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    sync_statuses: Optional[str] = None,
    custom_fields_fields: Optional[dict] = None,
    custom_fields_operator: Optional[str] = None,
    date_on_or_after: Optional[str] = None,
    date_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of inventory transfers from ServiceTitan.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/transfers"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "number": number,
        "referenceNumber": reference_number,
        "batchId": batch_id,
        "fromInventoryLocationIds": from_inventory_location_ids,
        "toInventoryLocationIds": to_inventory_location_ids,
        "businessUnitIds": business_unit_ids,
        "syncStatuses": sync_statuses,
        "customFields.Fields": custom_fields_fields,
        "customFields.Operator": custom_fields_operator,
        "dateOnOrAfter": date_on_or_after,
        "dateBefore": date_before,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_transfer_custom_fields(
    custom_fields: list
) -> dict:
    """
    Update custom fields for inventory transfers.
    
    Args:
        custom_fields: List of custom field updates (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/transfers/custom-fields"

    request_body = {"customFields": custom_fields}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_transfer(
    transfer_id: str,
    external_data: Optional[dict] = None
) -> dict:
    """
    Update an existing inventory transfer.
    
    Args:
        transfer_id: ID of the transfer to update (required)
        external_data: External data update model
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/transfers/{transfer_id}"

    request_body = {}
    if external_data is not None:
        request_body["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Transfer {transfer_id} not found"}
        response.raise_for_status()
        return response.json()

# TRUCKS ENDPOINTS

@mcp.tool()
async def get_inventory_trucks(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    names: Optional[str] = None,
    technician_ids: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of inventory trucks from ServiceTitan.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/trucks"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "names": names,
        "technicianIds": technician_ids,
        "businessUnitIds": business_unit_ids,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_truck(
    truck_id: str,
    external_data: Optional[dict] = None
) -> dict:
    """
    Update an existing inventory truck.
    
    Args:
        truck_id: ID of the truck to update (required)
        external_data: External data update model
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/trucks/{truck_id}"

    request_body = {}
    if external_data is not None:
        request_body["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Truck {truck_id} not found"}
        response.raise_for_status()
        return response.json()

# VENDORS ENDPOINTS

@mcp.tool()
async def create_inventory_vendor(
    name: str,
    address: Optional[dict] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    contact_name: Optional[str] = None,
    active: Optional[bool] = True,
    external_data: Optional[dict] = None
) -> dict:
    """
    Create a new vendor in ServiceTitan inventory.
    
    Args:
        name: Name of the vendor (required)
        address: Address information for the vendor
        phone: Phone number
        email: Email address
        contact_name: Contact person name
        active: Whether the vendor is active
        external_data: External data to attach
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/vendors"

    request_body = {"name": name}

    if address is not None:
        request_body["address"] = address
    if phone is not None:
        request_body["phone"] = phone
    if email is not None:
        request_body["email"] = email
    if contact_name is not None:
        request_body["contactName"] = contact_name
    if active is not None:
        request_body["active"] = active
    if external_data is not None:
        request_body["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_inventory_vendors(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    names: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of vendors from ServiceTitan inventory.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/vendors"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "names": names,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_inventory_vendor_by_id(
    vendor_id: str,
    external_data_application_guid: Optional[str] = None
) -> dict:
    """
    Get a specific vendor by ID.
    
    Args:
        vendor_id: ID of the vendor (required)
        external_data_application_guid: GUID for external data filtering
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/vendors/{vendor_id}"

    params = {}
    if external_data_application_guid is not None:
        params["externalDataApplicationGuid"] = external_data_application_guid

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return {"error": f"Vendor {vendor_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_vendor(
    vendor_id: str,
    name: Optional[str] = None,
    address: Optional[dict] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    contact_name: Optional[str] = None,
    active: Optional[bool] = None,
    external_data: Optional[dict] = None
) -> dict:
    """
    Update an existing vendor.
    
    Args:
        vendor_id: ID of the vendor to update (required)
        name: Name of the vendor
        address: Address information for the vendor
        phone: Phone number
        email: Email address
        contact_name: Contact person name
        active: Whether the vendor is active
        external_data: External data update model
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/vendors/{vendor_id}"

    request_body = {}

    if name is not None:
        request_body["name"] = name
    if address is not None:
        request_body["address"] = address
    if phone is not None:
        request_body["phone"] = phone
    if email is not None:
        request_body["email"] = email
    if contact_name is not None:
        request_body["contactName"] = contact_name
    if active is not None:
        request_body["active"] = active
    if external_data is not None:
        request_body["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Vendor {vendor_id} not found"}
        response.raise_for_status()
        return response.json()

# WAREHOUSES ENDPOINTS

@mcp.tool()
async def get_inventory_warehouses(
    ids: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None,
    names: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> dict:
    """
    Get a list of warehouses from ServiceTitan inventory.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/warehouses"

    params = {
        "ids": ids,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values,
        "names": names,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_inventory_warehouse(
    warehouse_id: str,
    external_data: Optional[dict] = None
) -> dict:
    """
    Update an existing warehouse.
    
    Args:
        warehouse_id: ID of the warehouse to update (required)
        external_data: External data update model
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/warehouses/{warehouse_id}"

    request_body = {}
    if external_data is not None:
        request_body["externalData"] = external_data

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Warehouse {warehouse_id} not found"}
        response.raise_for_status()
        return response.json()

# EXPORT ENDPOINTS

@mcp.tool()
async def export_inventory_adjustments() -> dict:
    """
    Export inventory adjustments data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/export/adjustments"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_inventory_purchase_orders() -> dict:
    """
    Export purchase orders data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/export/purchase-orders"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_inventory_returns() -> dict:
    """
    Export inventory returns data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/export/returns"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_inventory_transfers() -> dict:
    """
    Export inventory transfers data.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/inventory/v2/tenant/{TENANT_ID}/export/transfers"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
