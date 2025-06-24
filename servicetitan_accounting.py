#!/usr/bin/env python3
"""
ServiceTitan Accounting v2 API MCP Server

This server provides access to ServiceTitan's Accounting v2 API endpoints,
including accounts payable, general ledger, invoicing, payments, and journal entries.

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
API_BASE_URL = "https://api.servicetitan.io/accounting/v2"

# Global variables for token management
_access_token = None
_token_expires_at = 0

mcp = FastMCP("servicetitan-accounting")

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

# ACCOUNTS PAYABLE CREDITS
@mcp.tool()
async def get_ap_credits(
    ids: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a paginated list of accounts payable credits.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        sort: Applies sorting by specified fields
    
    Returns:
        Dictionary containing AP credits data
    """
    params = {}
    if ids: params["ids"] = ids
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/ap-credits", params=params)

@mcp.tool()
async def mark_ap_credits_as_exported(ap_credit_ids: List[int]) -> Dict[str, Any]:
    """
    Mark AP credits as exported.
    
    Args:
        ap_credit_ids: List of AP credit IDs to mark as exported
    
    Returns:
        Dictionary containing export results
    """
    data = [{"apCreditId": credit_id} for credit_id in ap_credit_ids]
    return await make_api_request("POST", "/ap-credits/markasexported", data=data)

# ACCOUNTS PAYABLE PAYMENTS
@mcp.tool()
async def get_ap_payments(
    ids: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a paginated list of accounts payable payments.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        sort: Applies sorting by specified fields
    
    Returns:
        Dictionary containing AP payments data
    """
    params = {}
    if ids: params["ids"] = ids
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/ap-payments", params=params)

@mcp.tool()
async def mark_ap_payments_as_exported(
    ap_payment_exports: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Mark AP payments as exported.
    
    Args:
        ap_payment_exports: List of payment export objects with apPaymentId, externalId, externalMessage
    
    Returns:
        Dictionary containing export results
    """
    return await make_api_request("POST", "/ap-payments/markasexported", data=ap_payment_exports)

# EXPORT ENDPOINTS
@mcp.tool()
async def export_invoices(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Provides export feed for invoices.
    
    Args:
        from_token: Continuation token from previous export or custom date (e.g., "2020-01-01")
        include_recent_changes: Use "true" to receive most recent changes quicker
    
    Returns:
        Dictionary containing invoice export data
    """
    params = {}
    if from_token: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    return await make_api_request("GET", "/export/invoices", params=params)

@mcp.tool()
async def export_invoice_items(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Provides export feed for invoice items.
    
    Args:
        from_token: Continuation token from previous export or custom date (e.g., "2020-01-01")
        include_recent_changes: Use "true" to receive most recent changes quicker
    
    Returns:
        Dictionary containing invoice items export data
    """
    params = {}
    if from_token: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    return await make_api_request("GET", "/export/invoice-items", params=params)

@mcp.tool()
async def export_payments(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Provides export feed for payments.
    
    Args:
        from_token: Continuation token from previous export or custom date (e.g., "2020-01-01")
        include_recent_changes: Use "true" to receive most recent changes quicker
    
    Returns:
        Dictionary containing payments export data
    """
    params = {}
    if from_token: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    return await make_api_request("GET", "/export/payments", params=params)

@mcp.tool()
async def export_inventory_bills(
    from_token: Optional[str] = None,
    include_recent_changes: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Provides export feed for inventory bills.
    
    Args:
        from_token: Continuation token from previous export or custom date (e.g., "2020-01-01")
        include_recent_changes: Use "true" to receive most recent changes quicker
    
    Returns:
        Dictionary containing inventory bills export data
    """
    params = {}
    if from_token: params["from"] = from_token
    if include_recent_changes is not None: params["includeRecentChanges"] = include_recent_changes
    
    return await make_api_request("GET", "/export/inventory-bills", params=params)

# GENERAL LEDGER ACCOUNTS
@mcp.tool()
async def get_gl_accounts(
    ids: Optional[str] = None,
    names: Optional[str] = None,
    numbers: Optional[str] = None,
    types: Optional[str] = None,
    subtypes: Optional[str] = None,
    description: Optional[str] = None,
    source: Optional[str] = None,
    active: Optional[str] = "True",
    is_intacct_group: Optional[bool] = None,
    is_intacct_bank_account: Optional[bool] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve General Ledger accounts that match the given criteria.
    
    Args:
        ids: Comma-delimited list of account IDs, maximum 50 items
        names: Comma-delimited list of account names, maximum 50 items
        numbers: Comma-delimited list of account numbers, maximum 50 items
        types: Comma-delimited list of account types, maximum 50 items
        subtypes: Comma-delimited list of account subtypes, maximum 50 items
        description: A substring that must be contained in the account description
        source: Account source (Undefined, AccountingSystem, ManuallyCreated, PublicApi)
        active: Specify if only active accounts should be retrieved (True, Any, False)
        is_intacct_group: Set to true to retrieve Intacct group accounts only
        is_intacct_bank_account: Set to true to retrieve Intacct bank accounts only
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Applies sorting by specified fields
    
    Returns:
        Dictionary containing General Ledger accounts data
    """
    params = {}
    if ids: params["ids"] = ids
    if names: params["names"] = names
    if numbers: params["numbers"] = numbers
    if types: params["types"] = types
    if subtypes: params["subtypes"] = subtypes
    if description: params["description"] = description
    if source: params["source"] = source
    if active: params["active"] = active
    if is_intacct_group is not None: params["isIntacctGroup"] = is_intacct_group
    if is_intacct_bank_account is not None: params["isIntacctBankAccount"] = is_intacct_bank_account
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/gl-accounts", params=params)

@mcp.tool()
async def create_gl_account(
    name: str,
    number: str,
    description: str,
    account_type: str,
    subtype: str
) -> Dict[str, Any]:
    """
    Create a new General Ledger account.
    
    Args:
        name: Account name
        number: Account number
        description: Account description
        account_type: Account type
        subtype: Account subtype
    
    Returns:
        Dictionary containing created GL account data
    """
    data = {
        "name": name,
        "number": number,
        "description": description,
        "type": account_type,
        "subtype": subtype
    }
    
    return await make_api_request("POST", "/gl-accounts", data=data)

@mcp.tool()
async def get_gl_account_by_id(account_id: int) -> Dict[str, Any]:
    """
    Retrieve single General Ledger account by account ID.
    
    Args:
        account_id: Long integer ID of the General Ledger account to be retrieved
    
    Returns:
        Dictionary containing General Ledger account data
    """
    return await make_api_request("GET", f"/gl-accounts/{account_id}")

@mcp.tool()
async def update_gl_account(
    account_id: int,
    name: Optional[str] = None,
    number: Optional[str] = None,
    description: Optional[str] = None,
    account_type: Optional[str] = None,
    subtype: Optional[str] = None,
    active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update General Ledger account. Can also deactivate the account (soft delete).
    
    Args:
        account_id: Long integer ID of the General Ledger account to be updated
        name: Account name
        number: Account number
        description: Account description
        account_type: Account type
        subtype: Account subtype
        active: Whether the account is active
    
    Returns:
        Dictionary containing updated General Ledger account data
    """
    data = {}
    if name is not None: data["name"] = name
    if number is not None: data["number"] = number
    if description is not None: data["description"] = description
    if account_type is not None: data["type"] = account_type
    if subtype is not None: data["subtype"] = subtype
    if active is not None: data["active"] = active
    
    return await make_api_request("PATCH", f"/gl-accounts/{account_id}", data=data)

@mcp.tool()
async def get_gl_account_types(
    ids: Optional[str] = None,
    names: Optional[str] = None,
    active: Optional[str] = "True",
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve General Ledger account types that match the given criteria.
    
    Args:
        ids: Comma-delimited list of account type IDs, maximum 50 items
        names: Comma-delimited list of account type names, maximum 50 items
        active: What kind of items should be returned (True, Any, False)
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Applies sorting by specified fields
    
    Returns:
        Dictionary containing General Ledger account types data
    """
    params = {}
    if ids: params["ids"] = ids
    if names: params["names"] = names
    if active: params["active"] = active
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/gl-accounts/types", params=params)

# INVENTORY BILLS
@mcp.tool()
async def get_inventory_bills(
    ids: Optional[str] = None,
    batch_id: Optional[int] = None,
    batch_number: Optional[int] = None,
    bill_number: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    job_number: Optional[str] = None,
    purchase_order_number: Optional[str] = None,
    purchase_order_types: Optional[str] = None,
    sync_statuses: Optional[List[str]] = None,
    min_cost: Optional[float] = None,
    max_cost: Optional[float] = None,
    bill_type: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    include_total: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get a list of inventory bills.
    
    Args:
        ids: Comma-delimited list of inventory bill IDs
        batch_id: Batch ID filter
        batch_number: Batch number filter
        bill_number: Bill number filter
        business_unit_ids: Business unit IDs filter
        date_from: Date from filter
        date_to: Date to filter
        job_number: Job number filter
        purchase_order_number: Purchase order number filter
        purchase_order_types: Purchase order types filter
        sync_statuses: Array of sync statuses
        min_cost: Minimum cost filter
        max_cost: Maximum cost filter
        bill_type: Bill type (NotSet, Procurement, ApBill, RecurringBill)
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        include_total: Whether total count should be returned
    
    Returns:
        Dictionary containing inventory bills data
    """
    params = {}
    if ids: params["ids"] = ids
    if batch_id: params["batchId"] = batch_id
    if batch_number: params["batchNumber"] = batch_number
    if bill_number: params["billNumber"] = bill_number
    if business_unit_ids: params["businessUnitIds"] = business_unit_ids
    if date_from: params["dateFrom"] = date_from
    if date_to: params["dateTo"] = date_to
    if job_number: params["jobNumber"] = job_number
    if purchase_order_number: params["purchaseOrderNumber"] = purchase_order_number
    if purchase_order_types: params["purchaseOrderTypes"] = purchase_order_types
    if sync_statuses: params["syncStatuses"] = sync_statuses
    if min_cost: params["minCost"] = min_cost
    if max_cost: params["maxCost"] = max_cost
    if bill_type: params["billType"] = bill_type
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if include_total: params["includeTotal"] = include_total
    
    return await make_api_request("GET", "/inventory-bills", params=params)

@mcp.tool()
async def get_inventory_bills_paginated(
    ids: Optional[str] = None,
    batch_id: Optional[int] = None,
    batch_number: Optional[int] = None,
    bill_number: Optional[str] = None,
    business_unit_ids: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    job_number: Optional[str] = None,
    purchase_order_number: Optional[str] = None,
    purchase_order_types: Optional[str] = None,
    sync_statuses: Optional[List[str]] = None,
    min_cost: Optional[float] = None,
    max_cost: Optional[float] = None,
    bill_type: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    include_total: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get a paginated list of inventory bills.
    
    Args:
        (Same as get_inventory_bills)
    
    Returns:
        Dictionary containing paginated inventory bills data
    """
    params = {}
    if ids: params["ids"] = ids
    if batch_id: params["batchId"] = batch_id
    if batch_number: params["batchNumber"] = batch_number
    if bill_number: params["billNumber"] = bill_number
    if business_unit_ids: params["businessUnitIds"] = business_unit_ids
    if date_from: params["dateFrom"] = date_from
    if date_to: params["dateTo"] = date_to
    if job_number: params["jobNumber"] = job_number
    if purchase_order_number: params["purchaseOrderNumber"] = purchase_order_number
    if purchase_order_types: params["purchaseOrderTypes"] = purchase_order_types
    if sync_statuses: params["syncStatuses"] = sync_statuses
    if min_cost: params["minCost"] = min_cost
    if max_cost: params["maxCost"] = max_cost
    if bill_type: params["billType"] = bill_type
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if include_total: params["includeTotal"] = include_total
    
    return await make_api_request("GET", "/inventory-bills/paginated", params=params)

@mcp.tool()
async def get_inventory_bills_custom_fields(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Return a paginated list of filtered custom field types available for inventory bills.
    
    Args:
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        sort: Sort by field
    
    Returns:
        Dictionary containing custom field types data
    """
    params = {}
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/inventory-bills/custom-fields", params=params)

@mcp.tool()
async def update_inventory_bills_custom_fields(
    operations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update custom fields for specified inventory bills.
    
    Args:
        operations: List of operations with objectId and customFields
    
    Returns:
        Dictionary containing update results
    """
    data = {"operations": operations}
    return await make_api_request("PATCH", "/inventory-bills/custom-fields", data=data)

@mcp.tool()
async def mark_inventory_bills_as_exported(
    inventory_bill_ids: List[int]
) -> Dict[str, Any]:
    """
    Mark inventory bills as exported.
    
    Args:
        inventory_bill_ids: List of inventory bill IDs to mark as exported
    
    Returns:
        Dictionary containing export results
    """
    data = {"inventoryBillIds": inventory_bill_ids}
    return await make_api_request("POST", "/inventory-bills/markasexported", data=data)

# INVOICES
@mcp.tool()
async def get_invoices(
    ids: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    statuses: Optional[List[str]] = None,
    batch_id: Optional[int] = None,
    batch_number: Optional[int] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    job_id: Optional[int] = None,
    job_number: Optional[str] = None,
    business_unit_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    invoiced_on_or_after: Optional[str] = None,
    invoiced_on_before: Optional[str] = None,
    adjustment_to_id: Optional[int] = None,
    number: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    total_greater: Optional[float] = None,
    total_less: Optional[float] = None,
    due_date_before: Optional[str] = None,
    due_date_on_or_after: Optional[str] = None,
    order_by: Optional[str] = None,
    order_by_direction: Optional[str] = None,
    review_statuses: Optional[List[str]] = None,
    assigned_to_ids: Optional[List[int]] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve a list of invoices. By default, all invoices will be returned regardless of status.
    
    Args:
        ids: Comma-delimited list of invoice IDs
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        statuses: Transaction status (Pending, Posted, Exported)
        batch_id: Batch ID associated with invoices
        batch_number: Batch number associated with invoices
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        job_id: Job ID associated with invoices
        job_number: Job number associated with invoices
        business_unit_id: Business unit ID associated with invoices
        customer_id: Customer ID associated with invoices
        invoiced_on_or_after: Invoiced on or after date
        invoiced_on_before: Invoiced on before date
        adjustment_to_id: When searching for adjustment invoices
        number: Reference number associated with invoices
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        created_before: Return items created before certain date/time (in UTC)
        total_greater: Retrieve invoices with total greater than or equal to value
        total_less: Retrieve invoices with total less than or equal to value
        due_date_before: Retrieve invoices with due date before value
        due_date_on_or_after: Retrieve invoices with due date on or after value
        order_by: Field to order the returned list
        order_by_direction: Order direction (desc/descending or asc/ascending)
        review_statuses: Review statuses associated with invoices
        assigned_to_ids: AssignedTo IDs associated with invoices
        sort: Applies sorting by specified field
    
    Returns:
        Dictionary containing invoices data
    """
    params = {}
    if ids: params["ids"] = ids
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if statuses: params["statuses"] = statuses
    if batch_id: params["batchId"] = batch_id
    if batch_number: params["batchNumber"] = batch_number
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if job_id: params["jobId"] = job_id
    if job_number: params["jobNumber"] = job_number
    if business_unit_id: params["businessUnitId"] = business_unit_id
    if customer_id: params["customerId"] = customer_id
    if invoiced_on_or_after: params["invoicedOnOrAfter"] = invoiced_on_or_after
    if invoiced_on_before: params["invoicedOnBefore"] = invoiced_on_before
    if adjustment_to_id: params["adjustmentToId"] = adjustment_to_id
    if number: params["number"] = number
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if created_before: params["createdBefore"] = created_before
    if total_greater: params["totalGreater"] = total_greater
    if total_less: params["totalLess"] = total_less
    if due_date_before: params["dueDateBefore"] = due_date_before
    if due_date_on_or_after: params["dueDateOnOrAfter"] = due_date_on_or_after
    if order_by: params["orderBy"] = order_by
    if order_by_direction: params["orderByDirection"] = order_by_direction
    if review_statuses: params["reviewStatuses"] = review_statuses
    if assigned_to_ids: params["assignedToIds"] = assigned_to_ids
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/invoices", params=params)

@mcp.tool()
async def create_adjustment_invoice(
    adjustment_to_id: int,
    number: Optional[str] = None,
    type_id: Optional[int] = None,
    invoiced_on: Optional[str] = None,
    subtotal: Optional[float] = None,
    tax: Optional[float] = None,
    summary: Optional[str] = None,
    items: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Create adjustment invoice.
    
    Args:
        adjustment_to_id: ID of invoice being adjusted
        number: Invoice number
        type_id: Invoice type ID
        invoiced_on: Invoice date
        subtotal: Subtotal amount
        tax: Tax amount
        summary: Invoice summary
        items: List of invoice items
    
    Returns:
        Dictionary containing created invoice ID
    """
    data = {"adjustmentToId": adjustment_to_id}
    if number is not None: data["number"] = number
    if type_id is not None: data["typeId"] = type_id
    if invoiced_on is not None: data["invoicedOn"] = invoiced_on
    if subtotal is not None: data["subtotal"] = subtotal
    if tax is not None: data["tax"] = tax
    if summary is not None: data["summary"] = summary
    if items is not None: data["items"] = items
    
    return await make_api_request("POST", "/invoices", data=data)

@mcp.tool()
async def update_invoice(
    invoice_id: int,
    number: Optional[str] = None,
    type_id: Optional[int] = None,
    invoiced_on: Optional[str] = None,
    subtotal: Optional[float] = None,
    tax: Optional[float] = None,
    summary: Optional[str] = None,
    due_date: Optional[str] = None,
    items: Optional[List[Dict[str, Any]]] = None,
    payments: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Update invoice.
    
    Args:
        invoice_id: Invoice ID to update
        number: Invoice number
        type_id: Invoice type ID
        invoiced_on: Invoice date
        subtotal: Subtotal amount
        tax: Tax amount
        summary: Invoice summary
        due_date: Due date
        items: List of invoice items
        payments: List of payments
    
    Returns:
        Dictionary containing update results
    """
    data = {}
    if number is not None: data["number"] = number
    if type_id is not None: data["typeId"] = type_id
    if invoiced_on is not None: data["invoicedOn"] = invoiced_on
    if subtotal is not None: data["subtotal"] = subtotal
    if tax is not None: data["tax"] = tax
    if summary is not None: data["summary"] = summary
    if due_date is not None: data["dueDate"] = due_date
    if items is not None: data["items"] = items
    if payments is not None: data["payments"] = payments
    
    return await make_api_request("PATCH", f"/invoices/{invoice_id}", data=data)

@mcp.tool()
async def update_invoice_items(
    invoice_id: int,
    sku_id: Optional[int] = None,
    sku_name: Optional[str] = None,
    technician_id: Optional[int] = None,
    description: Optional[str] = None,
    quantity: Optional[float] = None,
    unit_price: Optional[float] = None,
    cost: Optional[float] = None,
    is_add_on: Optional[bool] = None,
    item_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Update invoice items.
    
    Args:
        invoice_id: Invoice ID
        sku_id: SKU ID
        sku_name: SKU name
        technician_id: Technician ID
        description: Item description
        quantity: Item quantity
        unit_price: Unit price
        cost: Item cost
        is_add_on: Whether item is an add-on
        item_id: Item ID
    
    Returns:
        Dictionary containing update results
    """
    data = {}
    if sku_id is not None: data["skuId"] = sku_id
    if sku_name is not None: data["skuName"] = sku_name
    if technician_id is not None: data["technicianId"] = technician_id
    if description is not None: data["description"] = description
    if quantity is not None: data["quantity"] = quantity
    if unit_price is not None: data["unitPrice"] = unit_price
    if cost is not None: data["cost"] = cost
    if is_add_on is not None: data["isAddOn"] = is_add_on
    if item_id is not None: data["id"] = item_id
    
    return await make_api_request("PATCH", f"/invoices/{invoice_id}/items", data=data)

@mcp.tool()
async def delete_invoice_item(invoice_id: int, item_id: int) -> Dict[str, Any]:
    """
    Delete invoice item.
    
    Args:
        invoice_id: Invoice ID
        item_id: Item ID to delete
    
    Returns:
        Dictionary containing deletion results
    """
    return await make_api_request("DELETE", f"/invoices/{invoice_id}/items/{item_id}")

@mcp.tool()
async def mark_invoices_as_exported(
    invoice_exports: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Mark invoices as exported.
    
    Args:
        invoice_exports: List of invoice export objects with invoiceId, externalId, externalMessage
    
    Returns:
        Dictionary containing export results
    """
    return await make_api_request("POST", "/invoices/markasexported", data=invoice_exports)

@mcp.tool()
async def get_invoices_custom_fields(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Return a paginated list of filtered custom field types available for invoices.
    
    Args:
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        sort: Sort by field
    
    Returns:
        Dictionary containing custom field types data
    """
    params = {}
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/invoices/custom-fields", params=params)

@mcp.tool()
async def update_invoices_custom_fields(
    operations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update custom fields for specified invoices.
    
    Args:
        operations: List of operations with objectId and customFields
    
    Returns:
        Dictionary containing update results
    """
    data = {"operations": operations}
    return await make_api_request("PATCH", "/invoices/custom-fields", data=data)

# JOURNAL ENTRIES
@mcp.tool()
async def get_journal_entries(
    ids: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a paginated list of journal entries.
    
    Args:
        ids: Perform lookup by multiple IDs (maximum 50)
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        sort: Applies sorting by specified fields
    
    Returns:
        Dictionary containing journal entries data
    """
    params = {}
    if ids: params["ids"] = ids
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/journal-entries", params=params)

@mcp.tool()
async def create_journal_entry(
    memo: str,
    date: str,
    gl_account_debits: List[Dict[str, Any]],
    gl_account_credits: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create a new journal entry.
    
    Args:
        memo: Journal entry memo/description
        date: Journal entry date
        gl_account_debits: List of debit GL account entries
        gl_account_credits: List of credit GL account entries
    
    Returns:
        Dictionary containing created journal entry data
    """
    data = {
        "memo": memo,
        "date": date,
        "glAccountDebits": gl_account_debits,
        "glAccountCredits": gl_account_credits
    }
    
    return await make_api_request("POST", "/journal-entries", data=data)

@mcp.tool()
async def get_journal_entry_by_id(journal_entry_id: int) -> Dict[str, Any]:
    """
    Retrieve single journal entry by ID.
    
    Args:
        journal_entry_id: Long integer ID of the journal entry to be retrieved
    
    Returns:
        Dictionary containing journal entry data
    """
    return await make_api_request("GET", f"/journal-entries/{journal_entry_id}")

@mcp.tool()
async def update_journal_entry(
    journal_entry_id: int,
    memo: Optional[str] = None,
    date: Optional[str] = None,
    gl_account_debits: Optional[List[Dict[str, Any]]] = None,
    gl_account_credits: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Update journal entry.
    
    Args:
        journal_entry_id: Journal entry ID to update
        memo: Journal entry memo/description
        date: Journal entry date
        gl_account_debits: List of debit GL account entries
        gl_account_credits: List of credit GL account entries
    
    Returns:
        Dictionary containing updated journal entry data
    """
    data = {}
    if memo is not None: data["memo"] = memo
    if date is not None: data["date"] = date
    if gl_account_debits is not None: data["glAccountDebits"] = gl_account_debits
    if gl_account_credits is not None: data["glAccountCredits"] = gl_account_credits
    
    return await make_api_request("PATCH", f"/journal-entries/{journal_entry_id}", data=data)

@mcp.tool()
async def delete_journal_entry(journal_entry_id: int) -> Dict[str, Any]:
    """
    Delete journal entry.
    
    Args:
        journal_entry_id: Journal entry ID to delete
    
    Returns:
        Dictionary containing deletion results
    """
    return await make_api_request("DELETE", f"/journal-entries/{journal_entry_id}")

@mcp.tool()
async def mark_journal_entries_as_exported(
    journal_entry_ids: List[int]
) -> Dict[str, Any]:
    """
    Mark journal entries as exported.
    
    Args:
        journal_entry_ids: List of journal entry IDs to mark as exported
    
    Returns:
        Dictionary containing export results
    """
    data = [{"journalEntryId": entry_id} for entry_id in journal_entry_ids]
    return await make_api_request("POST", "/journal-entries/markasexported", data=data)

# PAYMENTS
@mcp.tool()
async def get_payments(
    ids: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    statuses: Optional[List[str]] = None,
    batch_id: Optional[int] = None,
    batch_number: Optional[int] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    job_id: Optional[int] = None,
    job_number: Optional[str] = None,
    business_unit_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    received_on_or_after: Optional[str] = None,
    received_before: Optional[str] = None,
    invoice_id: Optional[int] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    type_ids: Optional[List[int]] = None,
    total_greater: Optional[float] = None,
    total_less: Optional[float] = None,
    deposited_on_or_after: Optional[str] = None,
    deposited_before: Optional[str] = None,
    is_deposited: Optional[bool] = None,
    memo: Optional[str] = None,
    reference_number: Optional[str] = None,
    order_by: Optional[str] = None,
    order_by_direction: Optional[str] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve a list of payments. By default, all payments will be returned regardless of status.
    
    Args:
        ids: Comma-delimited list of payment IDs
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        statuses: Transaction status (Pending, Posted, Exported)
        batch_id: Batch ID associated with payments
        batch_number: Batch number associated with payments
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        job_id: Job ID associated with payments
        job_number: Job number associated with payments
        business_unit_id: Business unit ID associated with payments
        customer_id: Customer ID associated with payments
        received_on_or_after: Received on or after date
        received_before: Received before date
        invoice_id: Invoice ID associated with payments
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        created_before: Return items created before certain date/time (in UTC)
        type_ids: Payment type IDs
        total_greater: Retrieve payments with total greater than or equal to value
        total_less: Retrieve payments with total less than or equal to value
        deposited_on_or_after: Deposited on or after date
        deposited_before: Deposited before date
        is_deposited: Whether payment is deposited
        memo: Payment memo
        reference_number: Payment reference number
        order_by: Field to order the returned list
        order_by_direction: Order direction (desc/descending or asc/ascending)
        sort: Applies sorting by specified field
    
    Returns:
        Dictionary containing payments data
    """
    params = {}
    if ids: params["ids"] = ids
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if statuses: params["statuses"] = statuses
    if batch_id: params["batchId"] = batch_id
    if batch_number: params["batchNumber"] = batch_number
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if job_id: params["jobId"] = job_id
    if job_number: params["jobNumber"] = job_number
    if business_unit_id: params["businessUnitId"] = business_unit_id
    if customer_id: params["customerId"] = customer_id
    if received_on_or_after: params["receivedOnOrAfter"] = received_on_or_after
    if received_before: params["receivedBefore"] = received_before
    if invoice_id: params["invoiceId"] = invoice_id
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if created_before: params["createdBefore"] = created_before
    if type_ids: params["typeIds"] = type_ids
    if total_greater: params["totalGreater"] = total_greater
    if total_less: params["totalLess"] = total_less
    if deposited_on_or_after: params["depositedOnOrAfter"] = deposited_on_or_after
    if deposited_before: params["depositedBefore"] = deposited_before
    if is_deposited is not None: params["isDeposited"] = is_deposited
    if memo: params["memo"] = memo
    if reference_number: params["referenceNumber"] = reference_number
    if order_by: params["orderBy"] = order_by
    if order_by_direction: params["orderByDirection"] = order_by_direction
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/payments", params=params)

@mcp.tool()
async def create_payment(
    invoice_id: int,
    type_id: int,
    received_on: str,
    total: float,
    memo: Optional[str] = None,
    reference_number: Optional[str] = None,
    is_deposited: Optional[bool] = None,
    deposited_on: Optional[str] = None,
    check_number: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new payment.
    
    Args:
        invoice_id: Invoice ID this payment is for
        type_id: Payment type ID
        received_on: Date payment was received
        total: Payment total amount
        memo: Payment memo
        reference_number: Payment reference number
        is_deposited: Whether payment is deposited
        deposited_on: Date payment was deposited
        check_number: Check number if applicable
    
    Returns:
        Dictionary containing created payment ID
    """
    data = {
        "invoiceId": invoice_id,
        "typeId": type_id,
        "receivedOn": received_on,
        "total": total
    }
    if memo is not None: data["memo"] = memo
    if reference_number is not None: data["referenceNumber"] = reference_number
    if is_deposited is not None: data["isDeposited"] = is_deposited
    if deposited_on is not None: data["depositedOn"] = deposited_on
    if check_number is not None: data["checkNumber"] = check_number
    
    return await make_api_request("POST", "/payments", data=data)

@mcp.tool()
async def update_payment(
    payment_id: int,
    type_id: Optional[int] = None,
    received_on: Optional[str] = None,
    total: Optional[float] = None,
    memo: Optional[str] = None,
    reference_number: Optional[str] = None,
    is_deposited: Optional[bool] = None,
    deposited_on: Optional[str] = None,
    check_number: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update payment.
    
    Args:
        payment_id: Payment ID to update
        type_id: Payment type ID
        received_on: Date payment was received
        total: Payment total amount
        memo: Payment memo
        reference_number: Payment reference number
        is_deposited: Whether payment is deposited
        deposited_on: Date payment was deposited
        check_number: Check number if applicable
    
    Returns:
        Dictionary containing update results
    """
    data = {}
    if type_id is not None: data["typeId"] = type_id
    if received_on is not None: data["receivedOn"] = received_on
    if total is not None: data["total"] = total
    if memo is not None: data["memo"] = memo
    if reference_number is not None: data["referenceNumber"] = reference_number
    if is_deposited is not None: data["isDeposited"] = is_deposited
    if deposited_on is not None: data["depositedOn"] = deposited_on
    if check_number is not None: data["checkNumber"] = check_number
    
    return await make_api_request("PATCH", f"/payments/{payment_id}", data=data)

@mcp.tool()
async def delete_payment(payment_id: int) -> Dict[str, Any]:
    """
    Delete payment.
    
    Args:
        payment_id: Payment ID to delete
    
    Returns:
        Dictionary containing deletion results
    """
    return await make_api_request("DELETE", f"/payments/{payment_id}")

@mcp.tool()
async def mark_payments_as_exported(
    payment_exports: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Mark payments as exported.
    
    Args:
        payment_exports: List of payment export objects with paymentId, externalId, externalMessage
    
    Returns:
        Dictionary containing export results
    """
    return await make_api_request("POST", "/payments/markasexported", data=payment_exports)

@mcp.tool()
async def get_payments_custom_fields(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Return a paginated list of filtered custom field types available for payments.
    
    Args:
        page: Page number (starting from 1)
        page_size: Records per page (50 by default)
        include_total: Whether total count should be returned
        created_before: Return items created before certain date/time (in UTC)
        created_on_or_after: Return items created on or after certain date/time (in UTC)
        modified_before: Return items modified before certain date/time (in UTC)
        modified_on_or_after: Return items modified on or after certain date/time (in UTC)
        sort: Sort by field
    
    Returns:
        Dictionary containing custom field types data
    """
    params = {}
    if page: params["page"] = page
    if page_size: params["pageSize"] = page_size
    if include_total: params["includeTotal"] = include_total
    if created_before: params["createdBefore"] = created_before
    if created_on_or_after: params["createdOnOrAfter"] = created_on_or_after
    if modified_before: params["modifiedBefore"] = modified_before
    if modified_on_or_after: params["modifiedOnOrAfter"] = modified_on_or_after
    if sort: params["sort"] = sort
    
    return await make_api_request("GET", "/payments/custom-fields", params=params)

@mcp.tool()
async def update_payments_custom_fields(
    operations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update custom fields for specified payments.
    
    Args:
        operations: List of operations with objectId and customFields
    
    Returns:
        Dictionary containing update results
    """
    data = {"operations": operations}
    return await make_api_request("PATCH", "/payments/custom-fields", data=data)

# Server startup
if __name__ == "__main__":
    mcp.run(transport="stdio")