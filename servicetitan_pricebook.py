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

# FastMCP instance for Pricebook v2 API
mcp = FastMCP("servicetitan-pricebook")

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

# PRICEBOOK V2 API ENDPOINTS

@mcp.tool()
async def get_materials(
    is_other_direct_cost: Optional[bool] = None,
    cost_type_ids: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None
) -> dict:
    """
    Retrieve materials from ServiceTitan pricebook with optional filters.
    
    Args:
        is_other_direct_cost: Filter by Is Other Direct Cost
        cost_type_ids: Filter by Cost Type Ids
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName for ascending, -FieldName for descending)
        ids: Lookup by multiple IDs (maximum 50)
        created_before: Return items created before date/time (RFC3339 format)
        created_on_or_after: Return items created on or after date/time (RFC3339 format)
        modified_before: Return items modified before date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after date/time (RFC3339 format)
        active: Filter by active status ("True", "Any", "False")
        external_data_application_guid: Filter by external data application GUID
        external_data_key: Filter by external data key
        external_data_values: Filter by external data values
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materials"

    params = {
        "isOtherDirectCost": is_other_direct_cost,
        "costTypeIds": cost_type_ids,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort,
        "ids": ids,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_services(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None
) -> dict:
    """
    Retrieve services from ServiceTitan pricebook with optional filters.
    
    Args:
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName for ascending, -FieldName for descending)
        ids: Lookup by multiple IDs (maximum 50)
        created_before: Return items created before date/time (RFC3339 format)
        created_on_or_after: Return items created on or after date/time (RFC3339 format)
        modified_before: Return items modified before date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after date/time (RFC3339 format)
        active: Filter by active status ("True", "Any", "False")
        external_data_application_guid: Filter by external data application GUID
        external_data_key: Filter by external data key
        external_data_values: Filter by external data values
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/services"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort,
        "ids": ids,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_material(
    code: str,
    description: str,
    display_name: Optional[str] = None,
    cost: Optional[float] = None,
    active: Optional[bool] = True,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    hours: Optional[float] = None,
    bonus: Optional[float] = None,
    commission_bonus: Optional[float] = None,
    pays_commission: Optional[bool] = None,
    deduct_as_job_cost: Optional[bool] = None,
    unit_of_measure: Optional[str] = None,
    is_inventory: Optional[bool] = None,
    account: Optional[str] = None,
    cost_of_sale_account: Optional[str] = None,
    asset_account: Optional[str] = None,
    intacct_gl_group_account: Optional[str] = None,
    taxable: Optional[bool] = None,
    primary_vendor: Optional[dict] = None,
    other_vendors: Optional[list] = None,
    assets: Optional[list] = None,
    categories: Optional[list] = None,
    external_data: Optional[dict] = None,
    is_configurable_material: Optional[bool] = None,
    chargeable_by_default: Optional[bool] = None,
    variation_materials: Optional[list] = None,
    is_other_direct_cost: Optional[bool] = False,
    cost_type_id: Optional[int] = None,
    budget_cost_code: Optional[str] = None,
    budget_cost_type: Optional[str] = None
) -> dict:
    """
    Create a new material in ServiceTitan pricebook.
    
    Args:
        code: Code for the SKU (required)
        description: Description on the SKU that is displayed with the item (required)
        display_name: Name that displays with the SKU
        cost: The cost paid to acquire the material
        active: Active shows if the SKU is active or inactive
        price: Price of this SKU sold
        member_price: The price if the item is sold to a member
        add_on_price: The price of the SKU is sold as an add-on item
        add_on_member_price: The price if the SKU is sold to a member as an add-on item
        hours: The number of hours associated with installing the material
        bonus: Flat rate bonus paid for this task
        commission_bonus: Percentage rate bonus paid for this task
        pays_commission: PaysCommissions shows if this task pays commission
        deduct_as_job_cost: Is this deducted as job cost
        unit_of_measure: The unit of measure used for this SKU
        is_inventory: Is this equipment a part of your inventory
        account: The accounting account assigned to this SKU
        cost_of_sale_account: Cost of sale account
        asset_account: Asset account
        intacct_gl_group_account: Intacct GL Group Name
        taxable: Is this SKU taxable
        primary_vendor: The primary vendor you use to acquire this SKU
        other_vendors: Other vendors that you might go to acquire this SKU
        assets: Images, videos or PDFs attached to SKU
        categories: Categories that this SKU belongs to
        external_data: External data items to attach to this entity
        is_configurable_material: Is this a Configurable Material
        chargeable_by_default: Is this Chargeable by default
        variation_materials: Variations to add
        is_other_direct_cost: Is Other Direct Cost (false by default)
        cost_type_id: The Cost Type of the Other Direct Cost
        budget_cost_code: The Budget CostCode segment for this entity
        budget_cost_type: The Budget CostType segment for this entity
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materials"

    # Build request body with only non-None values
    request_body = {
        "code": code,
        "description": description
    }

    # Add optional fields only if they are not None
    if display_name is not None:
        request_body["displayName"] = display_name
    if cost is not None:
        request_body["cost"] = cost
    if active is not None:
        request_body["active"] = active
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if hours is not None:
        request_body["hours"] = hours
    if bonus is not None:
        request_body["bonus"] = bonus
    if commission_bonus is not None:
        request_body["commissionBonus"] = commission_bonus
    if pays_commission is not None:
        request_body["paysCommission"] = pays_commission
    if deduct_as_job_cost is not None:
        request_body["deductAsJobCost"] = deduct_as_job_cost
    if unit_of_measure is not None:
        request_body["unitOfMeasure"] = unit_of_measure
    if is_inventory is not None:
        request_body["isInventory"] = is_inventory
    if account is not None:
        request_body["account"] = account
    if cost_of_sale_account is not None:
        request_body["costOfSaleAccount"] = cost_of_sale_account
    if asset_account is not None:
        request_body["assetAccount"] = asset_account
    if intacct_gl_group_account is not None:
        request_body["intacctGlGroupAccount"] = intacct_gl_group_account
    if taxable is not None:
        request_body["taxable"] = taxable
    if primary_vendor is not None:
        request_body["primaryVendor"] = primary_vendor
    if other_vendors is not None:
        request_body["otherVendors"] = other_vendors
    if assets is not None:
        request_body["assets"] = assets
    if categories is not None:
        request_body["categories"] = categories
    if external_data is not None:
        request_body["externalData"] = external_data
    if is_configurable_material is not None:
        request_body["isConfigurableMaterial"] = is_configurable_material
    if chargeable_by_default is not None:
        request_body["chargeableByDefault"] = chargeable_by_default
    if variation_materials is not None:
        request_body["variationMaterials"] = variation_materials
    if is_other_direct_cost is not None:
        request_body["isOtherDirectCost"] = is_other_direct_cost
    if cost_type_id is not None:
        request_body["costTypeId"] = cost_type_id
    if budget_cost_code is not None:
        request_body["budgetCostCode"] = budget_cost_code
    if budget_cost_type is not None:
        request_body["budgetCostType"] = budget_cost_type

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_material_cost_types() -> dict:
    """
    Retrieve available cost types for materials from ServiceTitan pricebook.
    
    Returns a paginated response containing cost types with their IDs and names.
    These cost types can be used when creating materials with isOtherDirectCost=True.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materials/costtypes"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_material_by_id(
    material_id: str,
    external_data_application_guid: Optional[str] = None
) -> dict:
    """
    Retrieve a specific material from ServiceTitan pricebook by ID.
    
    Args:
        material_id: The ID of the material to retrieve (required)
        external_data_application_guid: Optional GUID for filtering external data
    
    Returns:
        Material details including pricing, vendor info, categories, assets, and metadata.
        Returns an error dict if the material is not found.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materials/{material_id}"

    params = {}
    if external_data_application_guid is not None:
        params["externalDataApplicationGuid"] = external_data_application_guid

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return {"error": f"Material {material_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_material(
    material_id: str,
    code: Optional[str] = None,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    cost: Optional[float] = None,
    active: Optional[bool] = None,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    hours: Optional[float] = None,
    bonus: Optional[float] = None,
    commission_bonus: Optional[float] = None,
    pays_commission: Optional[bool] = None,
    deduct_as_job_cost: Optional[bool] = None,
    unit_of_measure: Optional[str] = None,
    is_inventory: Optional[bool] = None,
    account: Optional[str] = None,
    cost_of_sale_account: Optional[str] = None,
    asset_account: Optional[str] = None,
    intacct_gl_group_account: Optional[str] = None,
    taxable: Optional[bool] = None,
    primary_vendor: Optional[dict] = None,
    other_vendors: Optional[list] = None,
    assets: Optional[list] = None,
    categories: Optional[list] = None,
    external_data: Optional[dict] = None,
    is_configurable_material: Optional[bool] = None,
    chargeable_by_default: Optional[bool] = None,
    variation_materials: Optional[list] = None,
    cost_type_id: Optional[int] = None,
    budget_cost_code: Optional[str] = None,
    budget_cost_type: Optional[str] = None
) -> dict:
    """
    Update an existing material in ServiceTitan pricebook.
    
    Args:
        material_id: ID of the material to update (required)
        code: Code for the SKU
        display_name: Name that displays with the SKU
        description: Description on the SKU that is displayed with the item
        cost: The cost paid to acquire the material
        active: Active shows if the SKU is active or inactive
        price: Price of this SKU sold
        member_price: The price if the item is sold to a member
        add_on_price: The price of the SKU is sold as an add-on item
        add_on_member_price: The price if the SKU is sold to a member as an add-on item
        hours: The number of hours associated with installing the material
        bonus: Flat rate bonus paid for this task
        commission_bonus: Percentage rate bonus paid for this task
        pays_commission: PaysCommissions shows if this task pays commission
        deduct_as_job_cost: Is this deducted as job cost
        unit_of_measure: The unit of measure used for this SKU
        is_inventory: Is this material a part of your inventory
        account: The accounting account assigned to this SKU
        cost_of_sale_account: Cost of sale account
        asset_account: Asset account
        intacct_gl_group_account: Intacct GL Group Name
        taxable: Is this SKU taxable
        primary_vendor: The primary vendor you use to acquire this SKU
        other_vendors: Other vendors that you might go to acquire this SKU
        assets: Images, videos or PDFs attached to SKU
        categories: Categories that this SKU belongs to
        external_data: External data update model (includes patchMode)
        is_configurable_material: Is this a Configurable Material
        chargeable_by_default: Is this Chargeable by default
        variation_materials: Added Variations
        cost_type_id: The Cost Type of the Other Direct Cost
        budget_cost_code: The Budget CostCode segment for this entity
        budget_cost_type: The Budget CostType segment for this entity
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materials/{material_id}"

    # Build request body with only non-None values
    request_body = {}

    # Add optional fields only if they are not None
    if code is not None:
        request_body["code"] = code
    if display_name is not None:
        request_body["displayName"] = display_name
    if description is not None:
        request_body["description"] = description
    if cost is not None:
        request_body["cost"] = cost
    if active is not None:
        request_body["active"] = active
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if hours is not None:
        request_body["hours"] = hours
    if bonus is not None:
        request_body["bonus"] = bonus
    if commission_bonus is not None:
        request_body["commissionBonus"] = commission_bonus
    if pays_commission is not None:
        request_body["paysCommission"] = pays_commission
    if deduct_as_job_cost is not None:
        request_body["deductAsJobCost"] = deduct_as_job_cost
    if unit_of_measure is not None:
        request_body["unitOfMeasure"] = unit_of_measure
    if is_inventory is not None:
        request_body["isInventory"] = is_inventory
    if account is not None:
        request_body["account"] = account
    if cost_of_sale_account is not None:
        request_body["costOfSaleAccount"] = cost_of_sale_account
    if asset_account is not None:
        request_body["assetAccount"] = asset_account
    if intacct_gl_group_account is not None:
        request_body["intacctGlGroupAccount"] = intacct_gl_group_account
    if taxable is not None:
        request_body["taxable"] = taxable
    if primary_vendor is not None:
        request_body["primaryVendor"] = primary_vendor
    if other_vendors is not None:
        request_body["otherVendors"] = other_vendors
    if assets is not None:
        request_body["assets"] = assets
    if categories is not None:
        request_body["categories"] = categories
    if external_data is not None:
        request_body["externalData"] = external_data
    if is_configurable_material is not None:
        request_body["isConfigurableMaterial"] = is_configurable_material
    if chargeable_by_default is not None:
        request_body["chargeableByDefault"] = chargeable_by_default
    if variation_materials is not None:
        request_body["variationMaterials"] = variation_materials
    if cost_type_id is not None:
        request_body["costTypeId"] = cost_type_id
    if budget_cost_code is not None:
        request_body["budgetCostCode"] = budget_cost_code
    if budget_cost_type is not None:
        request_body["budgetCostType"] = budget_cost_type

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Material {material_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_service(
    code: str,
    description: str,
    display_name: Optional[str] = None,
    service_materials: Optional[list] = None,
    service_equipment: Optional[list] = None,
    recommendations: Optional[list] = None,
    upgrades: Optional[list] = None,
    warranty: Optional[dict] = None,
    categories: Optional[list] = None,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    taxable: Optional[bool] = None,
    account: Optional[str] = None,
    intacct_gl_group_account: Optional[str] = None,
    hours: Optional[float] = None,
    is_labor: Optional[bool] = None,
    assets: Optional[list] = None,
    active: Optional[bool] = True,
    cross_sale_group: Optional[str] = None,
    pays_commission: Optional[bool] = None,
    bonus: Optional[float] = None,
    commission_bonus: Optional[float] = None,
    external_data: Optional[dict] = None,
    budget_cost_code: Optional[str] = None,
    budget_cost_type: Optional[str] = None
) -> dict:
    """
    Create a new service in ServiceTitan pricebook.
    
    Args:
        code: Code for the SKU (required)
        description: Description on the SKU that is displayed with the item (required)
        display_name: Name that displays with the SKU
        service_materials: Array of materials linked to the service (e.g., [{"skuId": 123, "quantity": 2}])
        service_equipment: Array of equipment linked to the service (e.g., [{"skuId": 456, "quantity": 1}])
        recommendations: Recommended services and materials to include with this SKU
        upgrades: Upgrades that can be sold for this SKU
        warranty: Warranty info (e.g., {"duration": 12, "description": "1 year warranty"})
        categories: Categories that this SKU belongs to
        price: Price of this SKU sold
        member_price: The price if the item is sold to a member
        add_on_price: The price of the SKU is sold as an add-on item
        add_on_member_price: The price if the SKU is sold to a member as an add-on item
        taxable: Is this SKU taxable
        account: The accounting account assigned to this SKU
        intacct_gl_group_account: Intacct GL Group Name
        hours: Hours needed to complete this service
        is_labor: Is a labor service
        assets: Images, videos or PDFs attached to SKU
        active: Active shows if the SKU is active or inactive
        cross_sale_group: A grouping of similar items for tracking on Technical Performance Board
        pays_commission: True if this task pays commission
        bonus: Flat rate bonus paid for this task
        commission_bonus: Percentage rate bonus paid for this task
        external_data: External data items to attach to this entity
        budget_cost_code: The Budget CostCode segment for this entity
        budget_cost_type: The Budget CostType segment for this entity
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/services"

    # Build request body with required fields
    request_body = {
        "code": code,
        "description": description
    }

    # Add optional fields only if they are not None
    if display_name is not None:
        request_body["displayName"] = display_name
    if service_materials is not None:
        request_body["serviceMaterials"] = service_materials
    if service_equipment is not None:
        request_body["serviceEquipment"] = service_equipment
    if recommendations is not None:
        request_body["recommendations"] = recommendations
    if upgrades is not None:
        request_body["upgrades"] = upgrades
    if warranty is not None:
        request_body["warranty"] = warranty
    if categories is not None:
        request_body["categories"] = categories
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if taxable is not None:
        request_body["taxable"] = taxable
    if account is not None:
        request_body["account"] = account
    if intacct_gl_group_account is not None:
        request_body["intacctGlGroupAccount"] = intacct_gl_group_account
    if hours is not None:
        request_body["hours"] = hours
    if is_labor is not None:
        request_body["isLabor"] = is_labor
    if assets is not None:
        request_body["assets"] = assets
    if active is not None:
        request_body["active"] = active
    if cross_sale_group is not None:
        request_body["crossSaleGroup"] = cross_sale_group
    if pays_commission is not None:
        request_body["paysCommission"] = pays_commission
    if bonus is not None:
        request_body["bonus"] = bonus
    if commission_bonus is not None:
        request_body["commissionBonus"] = commission_bonus
    if external_data is not None:
        request_body["externalData"] = external_data
    if budget_cost_code is not None:
        request_body["budgetCostCode"] = budget_cost_code
    if budget_cost_type is not None:
        request_body["budgetCostType"] = budget_cost_type

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_service_by_id(
    service_id: str,
    external_data_application_guid: Optional[str] = None
) -> dict:
    """
    Retrieve a specific service from ServiceTitan pricebook by ID.
    
    Args:
        service_id: The ID of the service to retrieve (required)
        external_data_application_guid: Optional GUID for filtering external data
    
    Returns:
        Service details including pricing, warranty, materials, equipment, categories, 
        assets, recommendations, upgrades, and metadata.
        Returns an error dict if the service is not found.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/services/{service_id}"

    params = {}
    if external_data_application_guid is not None:
        params["externalDataApplicationGuid"] = external_data_application_guid

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return {"error": f"Service {service_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_service(
    service_id: str,
    code: Optional[str] = None,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    warranty: Optional[dict] = None,
    categories: Optional[list] = None,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    taxable: Optional[bool] = None,
    account: Optional[str] = None,
    intacct_gl_group_account: Optional[str] = None,
    hours: Optional[float] = None,
    is_labor: Optional[bool] = None,
    recommendations: Optional[list] = None,
    upgrades: Optional[list] = None,
    assets: Optional[list] = None,
    service_materials: Optional[list] = None,
    service_equipment: Optional[list] = None,
    active: Optional[bool] = None,
    cross_sale_group: Optional[str] = None,
    pays_commission: Optional[bool] = None,
    bonus: Optional[float] = None,
    commission_bonus: Optional[float] = None,
    external_data: Optional[dict] = None,
    budget_cost_code: Optional[str] = None,
    budget_cost_type: Optional[str] = None
) -> dict:
    """
    Update an existing service in ServiceTitan pricebook.
    
    Args:
        service_id: ID of the service to update (required)
        code: Code for the SKU
        display_name: Name that displays with the SKU
        description: Description on the SKU that is displayed with the item
        warranty: Warranty info (e.g., {"duration": 12, "description": "1 year warranty"})
        categories: Categories that this SKU belongs to
        price: Price of this SKU sold
        member_price: The price if the item is sold to a member
        add_on_price: The price of the SKU is sold as an add-on item
        add_on_member_price: The price if the SKU is sold to a member as an add-on item
        taxable: Is this SKU taxable
        account: The accounting account assigned to this SKU
        intacct_gl_group_account: Intacct GL Group Name
        hours: Hours needed to complete this service
        is_labor: Is a labor service
        recommendations: Recommended other services to include with this SKU
        upgrades: Upgrades that can be sold for this SKU
        assets: Images, videos or PDFs attached to SKU
        service_materials: Array of materials linked to the service (e.g., [{"skuId": 123, "quantity": 2}])
        service_equipment: Array of equipment linked to the service (e.g., [{"skuId": 456, "quantity": 1}])
        active: Active shows if the SKU is active or inactive
        cross_sale_group: A grouping of similar items for tracking on Technical Performance Board
        pays_commission: PaysCommissions shows if this task pays commission
        bonus: Flat rate bonus paid for this task
        commission_bonus: Percentage rate bonus paid for this task
        external_data: External data update model (includes patchMode)
        budget_cost_code: The Budget CostCode segment for this entity
        budget_cost_type: The Budget CostType segment for this entity
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/services/{service_id}"

    # Build request body with only non-None values
    request_body = {}

    # Add optional fields only if they are not None
    if code is not None:
        request_body["code"] = code
    if display_name is not None:
        request_body["displayName"] = display_name
    if description is not None:
        request_body["description"] = description
    if warranty is not None:
        request_body["warranty"] = warranty
    if categories is not None:
        request_body["categories"] = categories
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if taxable is not None:
        request_body["taxable"] = taxable
    if account is not None:
        request_body["account"] = account
    if intacct_gl_group_account is not None:
        request_body["intacctGlGroupAccount"] = intacct_gl_group_account
    if hours is not None:
        request_body["hours"] = hours
    if is_labor is not None:
        request_body["isLabor"] = is_labor
    if recommendations is not None:
        request_body["recommendations"] = recommendations
    if upgrades is not None:
        request_body["upgrades"] = upgrades
    if assets is not None:
        request_body["assets"] = assets
    if service_materials is not None:
        request_body["serviceMaterials"] = service_materials
    if service_equipment is not None:
        request_body["serviceEquipment"] = service_equipment
    if active is not None:
        request_body["active"] = active
    if cross_sale_group is not None:
        request_body["crossSaleGroup"] = cross_sale_group
    if pays_commission is not None:
        request_body["paysCommission"] = pays_commission
    if bonus is not None:
        request_body["bonus"] = bonus
    if commission_bonus is not None:
        request_body["commissionBonus"] = commission_bonus
    if external_data is not None:
        request_body["externalData"] = external_data
    if budget_cost_code is not None:
        request_body["budgetCostCode"] = budget_cost_code
    if budget_cost_type is not None:
        request_body["budgetCostType"] = budget_cost_type

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Service {service_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_material(material_id: str) -> dict:
    """
    Delete a material from ServiceTitan pricebook.
    
    Args:
        material_id: The ID of the material to delete (required)
    
    Returns:
        Success confirmation or error if material not found.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materials/{material_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Material {material_id} not found"}
        response.raise_for_status()
        return {"success": f"Material {material_id} deleted successfully"}

@mcp.tool()
async def delete_service(service_id: str) -> dict:
    """
    Delete a service from ServiceTitan pricebook.
    
    Args:
        service_id: The ID of the service to delete (required)
    
    Returns:
        Success confirmation or error if service not found.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/services/{service_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Service {service_id} not found"}
        response.raise_for_status()
        return {"success": f"Service {service_id} deleted successfully"}

# CATEGORIES ENDPOINTS

@mcp.tool()
async def get_categories(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None,
    category_type: Optional[str] = None,
    active: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None
) -> dict:
    """
    Retrieve categories from ServiceTitan pricebook.
    
    Args:
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName for ascending, -FieldName for descending)
        category_type: Category type ("Services", "Materials")
        active: Filter by active status ("True", "Any", "False")
        created_before: Return items created before date/time (RFC3339 format)
        created_on_or_after: Return items created on or after date/time (RFC3339 format)
        modified_before: Return items modified before date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after date/time (RFC3339 format)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/categories"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort,
        "categoryType": category_type,
        "active": active,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_category(
    name: str,
    active: Optional[bool] = True,
    description: Optional[str] = None,
    parent_id: Optional[int] = None,
    position: Optional[int] = None,
    image: Optional[str] = None,
    category_type: Optional[str] = None,
    business_unit_ids: Optional[list] = None,
    sku_images: Optional[list] = None,
    sku_videos: Optional[list] = None
) -> dict:
    """
    Create a new category in ServiceTitan pricebook.
    
    Args:
        name: Category name (required)
        active: Whether the category is active
        description: Category description
        parent_id: ID of parent category
        position: Position in category hierarchy
        image: Category image URL
        category_type: Type of category ("Services", "Materials")
        business_unit_ids: List of business unit IDs
        sku_images: List of SKU image URLs
        sku_videos: List of SKU video URLs
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/categories"

    request_body = {"name": name}

    if active is not None:
        request_body["active"] = active
    if description is not None:
        request_body["description"] = description
    if parent_id is not None:
        request_body["parentId"] = parent_id
    if position is not None:
        request_body["position"] = position
    if image is not None:
        request_body["image"] = image
    if category_type is not None:
        request_body["categoryType"] = category_type
    if business_unit_ids is not None:
        request_body["businessUnitIds"] = business_unit_ids
    if sku_images is not None:
        request_body["skuImages"] = sku_images
    if sku_videos is not None:
        request_body["skuVideos"] = sku_videos

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_category_by_id(category_id: str) -> dict:
    """
    Retrieve a specific category from ServiceTitan pricebook by ID.
    
    Args:
        category_id: The ID of the category to retrieve (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/categories/{category_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Category {category_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_category(
    category_id: str,
    name: Optional[str] = None,
    active: Optional[bool] = None,
    description: Optional[str] = None,
    parent_id: Optional[int] = None,
    position: Optional[int] = None,
    image: Optional[str] = None,
    category_type: Optional[str] = None,
    business_unit_ids: Optional[list] = None,
    sku_images: Optional[list] = None,
    sku_videos: Optional[list] = None
) -> dict:
    """
    Update an existing category in ServiceTitan pricebook.
    
    Args:
        category_id: ID of the category to update (required)
        name: Category name
        active: Whether the category is active
        description: Category description
        parent_id: ID of parent category
        position: Position in category hierarchy
        image: Category image URL
        category_type: Type of category ("Services", "Materials")
        business_unit_ids: List of business unit IDs
        sku_images: List of SKU image URLs
        sku_videos: List of SKU video URLs
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/categories/{category_id}"

    request_body = {}

    if name is not None:
        request_body["name"] = name
    if active is not None:
        request_body["active"] = active
    if description is not None:
        request_body["description"] = description
    if parent_id is not None:
        request_body["parentId"] = parent_id
    if position is not None:
        request_body["position"] = position
    if image is not None:
        request_body["image"] = image
    if category_type is not None:
        request_body["categoryType"] = category_type
    if business_unit_ids is not None:
        request_body["businessUnitIds"] = business_unit_ids
    if sku_images is not None:
        request_body["skuImages"] = sku_images
    if sku_videos is not None:
        request_body["skuVideos"] = sku_videos

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Category {category_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_category(category_id: str) -> dict:
    """
    Delete a category from ServiceTitan pricebook.
    
    Args:
        category_id: The ID of the category to delete (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/categories/{category_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Category {category_id} not found"}
        response.raise_for_status()
        return {"success": f"Category {category_id} deleted successfully"}

# EQUIPMENT ENDPOINTS

@mcp.tool()
async def get_equipment(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None
) -> dict:
    """
    Retrieve equipment from ServiceTitan pricebook with optional filters.
    
    Args:
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName for ascending, -FieldName for descending)
        ids: Lookup by multiple IDs (maximum 50)
        created_before: Return items created before date/time (RFC3339 format)
        created_on_or_after: Return items created on or after date/time (RFC3339 format)
        modified_before: Return items modified before date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after date/time (RFC3339 format)
        active: Filter by active status ("True", "Any", "False")
        external_data_application_guid: Filter by external data application GUID
        external_data_key: Filter by external data key
        external_data_values: Filter by external data values
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/equipment"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort,
        "ids": ids,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_equipment(
    code: str,
    description: str,
    display_name: Optional[str] = None,
    cost: Optional[float] = None,
    active: Optional[bool] = True,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    hours: Optional[float] = None,
    bonus: Optional[float] = None,
    commission_bonus: Optional[float] = None,
    pays_commission: Optional[bool] = None,
    deduct_as_job_cost: Optional[bool] = None,
    unit_of_measure: Optional[str] = None,
    is_inventory: Optional[bool] = None,
    account: Optional[str] = None,
    cost_of_sale_account: Optional[str] = None,
    asset_account: Optional[str] = None,
    intacct_gl_group_account: Optional[str] = None,
    taxable: Optional[bool] = None,
    primary_vendor: Optional[dict] = None,
    other_vendors: Optional[list] = None,
    assets: Optional[list] = None,
    categories: Optional[list] = None,
    external_data: Optional[dict] = None,
    budget_cost_code: Optional[str] = None,
    budget_cost_type: Optional[str] = None
) -> dict:
    """
    Create new equipment in ServiceTitan pricebook.
    
    Args:
        code: Code for the SKU (required)
        description: Description on the SKU that is displayed with the item (required)
        display_name: Name that displays with the SKU
        cost: The cost paid to acquire the equipment
        active: Active shows if the SKU is active or inactive
        price: Price of this SKU sold
        member_price: The price if the item is sold to a member
        add_on_price: The price of the SKU is sold as an add-on item
        add_on_member_price: The price if the SKU is sold to a member as an add-on item
        hours: The number of hours associated with installing the equipment
        bonus: Flat rate bonus paid for this task
        commission_bonus: Percentage rate bonus paid for this task
        pays_commission: PaysCommissions shows if this task pays commission
        deduct_as_job_cost: Is this deducted as job cost
        unit_of_measure: The unit of measure used for this SKU
        is_inventory: Is this equipment a part of your inventory
        account: The accounting account assigned to this SKU
        cost_of_sale_account: Cost of sale account
        asset_account: Asset account
        intacct_gl_group_account: Intacct GL Group Name
        taxable: Is this SKU taxable
        primary_vendor: The primary vendor you use to acquire this SKU
        other_vendors: Other vendors that you might go to acquire this SKU
        assets: Images, videos or PDFs attached to SKU
        categories: Categories that this SKU belongs to
        external_data: External data items to attach to this entity
        budget_cost_code: The Budget CostCode segment for this entity
        budget_cost_type: The Budget CostType segment for this entity
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/equipment"

    request_body = {
        "code": code,
        "description": description
    }

    if display_name is not None:
        request_body["displayName"] = display_name
    if cost is not None:
        request_body["cost"] = cost
    if active is not None:
        request_body["active"] = active
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if hours is not None:
        request_body["hours"] = hours
    if bonus is not None:
        request_body["bonus"] = bonus
    if commission_bonus is not None:
        request_body["commissionBonus"] = commission_bonus
    if pays_commission is not None:
        request_body["paysCommission"] = pays_commission
    if deduct_as_job_cost is not None:
        request_body["deductAsJobCost"] = deduct_as_job_cost
    if unit_of_measure is not None:
        request_body["unitOfMeasure"] = unit_of_measure
    if is_inventory is not None:
        request_body["isInventory"] = is_inventory
    if account is not None:
        request_body["account"] = account
    if cost_of_sale_account is not None:
        request_body["costOfSaleAccount"] = cost_of_sale_account
    if asset_account is not None:
        request_body["assetAccount"] = asset_account
    if intacct_gl_group_account is not None:
        request_body["intacctGlGroupAccount"] = intacct_gl_group_account
    if taxable is not None:
        request_body["taxable"] = taxable
    if primary_vendor is not None:
        request_body["primaryVendor"] = primary_vendor
    if other_vendors is not None:
        request_body["otherVendors"] = other_vendors
    if assets is not None:
        request_body["assets"] = assets
    if categories is not None:
        request_body["categories"] = categories
    if external_data is not None:
        request_body["externalData"] = external_data
    if budget_cost_code is not None:
        request_body["budgetCostCode"] = budget_cost_code
    if budget_cost_type is not None:
        request_body["budgetCostType"] = budget_cost_type

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_equipment_by_id(
    equipment_id: str,
    external_data_application_guid: Optional[str] = None
) -> dict:
    """
    Retrieve a specific equipment from ServiceTitan pricebook by ID.
    
    Args:
        equipment_id: The ID of the equipment to retrieve (required)
        external_data_application_guid: Optional GUID for filtering external data
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/equipment/{equipment_id}"

    params = {}
    if external_data_application_guid is not None:
        params["externalDataApplicationGuid"] = external_data_application_guid

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return {"error": f"Equipment {equipment_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_equipment(
    equipment_id: str,
    code: Optional[str] = None,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    cost: Optional[float] = None,
    active: Optional[bool] = None,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    hours: Optional[float] = None,
    bonus: Optional[float] = None,
    commission_bonus: Optional[float] = None,
    pays_commission: Optional[bool] = None,
    deduct_as_job_cost: Optional[bool] = None,
    unit_of_measure: Optional[str] = None,
    is_inventory: Optional[bool] = None,
    account: Optional[str] = None,
    cost_of_sale_account: Optional[str] = None,
    asset_account: Optional[str] = None,
    intacct_gl_group_account: Optional[str] = None,
    taxable: Optional[bool] = None,
    primary_vendor: Optional[dict] = None,
    other_vendors: Optional[list] = None,
    assets: Optional[list] = None,
    categories: Optional[list] = None,
    external_data: Optional[dict] = None,
    budget_cost_code: Optional[str] = None,
    budget_cost_type: Optional[str] = None
) -> dict:
    """
    Update an existing equipment in ServiceTitan pricebook.
    
    Args:
        equipment_id: ID of the equipment to update (required)
        code: Code for the SKU
        display_name: Name that displays with the SKU
        description: Description on the SKU that is displayed with the item
        cost: The cost paid to acquire the equipment
        active: Active shows if the SKU is active or inactive
        price: Price of this SKU sold
        member_price: The price if the item is sold to a member
        add_on_price: The price of the SKU is sold as an add-on item
        add_on_member_price: The price if the SKU is sold to a member as an add-on item
        hours: The number of hours associated with installing the equipment
        bonus: Flat rate bonus paid for this task
        commission_bonus: Percentage rate bonus paid for this task
        pays_commission: PaysCommissions shows if this task pays commission
        deduct_as_job_cost: Is this deducted as job cost
        unit_of_measure: The unit of measure used for this SKU
        is_inventory: Is this equipment a part of your inventory
        account: The accounting account assigned to this SKU
        cost_of_sale_account: Cost of sale account
        asset_account: Asset account
        intacct_gl_group_account: Intacct GL Group Name
        taxable: Is this SKU taxable
        primary_vendor: The primary vendor you use to acquire this SKU
        other_vendors: Other vendors that you might go to acquire this SKU
        assets: Images, videos or PDFs attached to SKU
        categories: Categories that this SKU belongs to
        external_data: External data update model (includes patchMode)
        budget_cost_code: The Budget CostCode segment for this entity
        budget_cost_type: The Budget CostType segment for this entity
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/equipment/{equipment_id}"

    request_body = {}

    if code is not None:
        request_body["code"] = code
    if display_name is not None:
        request_body["displayName"] = display_name
    if description is not None:
        request_body["description"] = description
    if cost is not None:
        request_body["cost"] = cost
    if active is not None:
        request_body["active"] = active
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if hours is not None:
        request_body["hours"] = hours
    if bonus is not None:
        request_body["bonus"] = bonus
    if commission_bonus is not None:
        request_body["commissionBonus"] = commission_bonus
    if pays_commission is not None:
        request_body["paysCommission"] = pays_commission
    if deduct_as_job_cost is not None:
        request_body["deductAsJobCost"] = deduct_as_job_cost
    if unit_of_measure is not None:
        request_body["unitOfMeasure"] = unit_of_measure
    if is_inventory is not None:
        request_body["isInventory"] = is_inventory
    if account is not None:
        request_body["account"] = account
    if cost_of_sale_account is not None:
        request_body["costOfSaleAccount"] = cost_of_sale_account
    if asset_account is not None:
        request_body["assetAccount"] = asset_account
    if intacct_gl_group_account is not None:
        request_body["intacctGlGroupAccount"] = intacct_gl_group_account
    if taxable is not None:
        request_body["taxable"] = taxable
    if primary_vendor is not None:
        request_body["primaryVendor"] = primary_vendor
    if other_vendors is not None:
        request_body["otherVendors"] = other_vendors
    if assets is not None:
        request_body["assets"] = assets
    if categories is not None:
        request_body["categories"] = categories
    if external_data is not None:
        request_body["externalData"] = external_data
    if budget_cost_code is not None:
        request_body["budgetCostCode"] = budget_cost_code
    if budget_cost_type is not None:
        request_body["budgetCostType"] = budget_cost_type

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Equipment {equipment_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_equipment(equipment_id: str) -> dict:
    """
    Delete equipment from ServiceTitan pricebook.
    
    Args:
        equipment_id: The ID of the equipment to delete (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/equipment/{equipment_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Equipment {equipment_id} not found"}
        response.raise_for_status()
        return {"success": f"Equipment {equipment_id} deleted successfully"}

# DISCOUNTS AND FEES ENDPOINTS

@mcp.tool()
async def get_discounts_and_fees(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    sort: Optional[str] = None,
    ids: Optional[str] = None,
    created_before: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    active: Optional[str] = None,
    external_data_application_guid: Optional[str] = None,
    external_data_key: Optional[str] = None,
    external_data_values: Optional[str] = None
) -> dict:
    """
    Retrieve discounts and fees from ServiceTitan pricebook.
    
    Args:
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
        sort: Sort by field (+FieldName for ascending, -FieldName for descending)
        ids: Lookup by multiple IDs (maximum 50)
        created_before: Return items created before date/time (RFC3339 format)
        created_on_or_after: Return items created on or after date/time (RFC3339 format)
        modified_before: Return items modified before date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after date/time (RFC3339 format)
        active: Filter by active status ("True", "Any", "False")
        external_data_application_guid: Filter by external data application GUID
        external_data_key: Filter by external data key
        external_data_values: Filter by external data values
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/discounts-and-fees"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "sort": sort,
        "ids": ids,
        "createdBefore": created_before,
        "createdOnOrAfter": created_on_or_after,
        "modifiedBefore": modified_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "active": active,
        "externalDataApplicationGuid": external_data_application_guid,
        "externalDataKey": external_data_key,
        "externalDataValues": external_data_values
    }

    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def create_discount_or_fee(
    code: str,
    description: str,
    discount_fee_type: str,
    display_name: Optional[str] = None,
    active: Optional[bool] = True,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    taxable: Optional[bool] = None,
    account: Optional[str] = None,
    intacct_gl_group_account: Optional[str] = None,
    assets: Optional[list] = None,
    categories: Optional[list] = None,
    external_data: Optional[dict] = None,
    budget_cost_code: Optional[str] = None,
    budget_cost_type: Optional[str] = None
) -> dict:
    """
    Create a new discount or fee in ServiceTitan pricebook.
    
    Args:
        code: Code for the SKU (required)
        description: Description on the SKU that is displayed with the item (required)
        discount_fee_type: Type of discount/fee (required - "Discount" or "Fee")
        display_name: Name that displays with the SKU
        active: Active shows if the SKU is active or inactive
        price: Price of this SKU sold
        member_price: The price if the item is sold to a member
        add_on_price: The price of the SKU is sold as an add-on item
        add_on_member_price: The price if the SKU is sold to a member as an add-on item
        taxable: Is this SKU taxable
        account: The accounting account assigned to this SKU
        intacct_gl_group_account: Intacct GL Group Name
        assets: Images, videos or PDFs attached to SKU
        categories: Categories that this SKU belongs to
        external_data: External data items to attach to this entity
        budget_cost_code: The Budget CostCode segment for this entity
        budget_cost_type: The Budget CostType segment for this entity
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/discounts-and-fees"

    request_body = {
        "code": code,
        "description": description,
        "type": discount_fee_type
    }

    if display_name is not None:
        request_body["displayName"] = display_name
    if active is not None:
        request_body["active"] = active
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if taxable is not None:
        request_body["taxable"] = taxable
    if account is not None:
        request_body["account"] = account
    if intacct_gl_group_account is not None:
        request_body["intacctGlGroupAccount"] = intacct_gl_group_account
    if assets is not None:
        request_body["assets"] = assets
    if categories is not None:
        request_body["categories"] = categories
    if external_data is not None:
        request_body["externalData"] = external_data
    if budget_cost_code is not None:
        request_body["budgetCostCode"] = budget_cost_code
    if budget_cost_type is not None:
        request_body["budgetCostType"] = budget_cost_type

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_discount_or_fee_by_id(
    discount_fee_id: str,
    external_data_application_guid: Optional[str] = None
) -> dict:
    """
    Retrieve a specific discount or fee from ServiceTitan pricebook by ID.
    
    Args:
        discount_fee_id: The ID of the discount/fee to retrieve (required)
        external_data_application_guid: Optional GUID for filtering external data
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/discounts-and-fees/{discount_fee_id}"

    params = {}
    if external_data_application_guid is not None:
        params["externalDataApplicationGuid"] = external_data_application_guid

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 404:
            return {"error": f"Discount/Fee {discount_fee_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_discount_or_fee(
    discount_fee_id: str,
    code: Optional[str] = None,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    discount_fee_type: Optional[str] = None,
    active: Optional[bool] = None,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    taxable: Optional[bool] = None,
    account: Optional[str] = None,
    intacct_gl_group_account: Optional[str] = None,
    assets: Optional[list] = None,
    categories: Optional[list] = None,
    external_data: Optional[dict] = None,
    budget_cost_code: Optional[str] = None,
    budget_cost_type: Optional[str] = None
) -> dict:
    """
    Update an existing discount or fee in ServiceTitan pricebook.
    
    Args:
        discount_fee_id: ID of the discount/fee to update (required)
        code: Code for the SKU
        display_name: Name that displays with the SKU
        description: Description on the SKU that is displayed with the item
        discount_fee_type: Type of discount/fee ("Discount" or "Fee")
        active: Active shows if the SKU is active or inactive
        price: Price of this SKU sold
        member_price: The price if the item is sold to a member
        add_on_price: The price of the SKU is sold as an add-on item
        add_on_member_price: The price if the SKU is sold to a member as an add-on item
        taxable: Is this SKU taxable
        account: The accounting account assigned to this SKU
        intacct_gl_group_account: Intacct GL Group Name
        assets: Images, videos or PDFs attached to SKU
        categories: Categories that this SKU belongs to
        external_data: External data update model (includes patchMode)
        budget_cost_code: The Budget CostCode segment for this entity
        budget_cost_type: The Budget CostType segment for this entity
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/discounts-and-fees/{discount_fee_id}"

    request_body = {}

    if code is not None:
        request_body["code"] = code
    if display_name is not None:
        request_body["displayName"] = display_name
    if description is not None:
        request_body["description"] = description
    if discount_fee_type is not None:
        request_body["type"] = discount_fee_type
    if active is not None:
        request_body["active"] = active
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if taxable is not None:
        request_body["taxable"] = taxable
    if account is not None:
        request_body["account"] = account
    if intacct_gl_group_account is not None:
        request_body["intacctGlGroupAccount"] = intacct_gl_group_account
    if assets is not None:
        request_body["assets"] = assets
    if categories is not None:
        request_body["categories"] = categories
    if external_data is not None:
        request_body["externalData"] = external_data
    if budget_cost_code is not None:
        request_body["budgetCostCode"] = budget_cost_code
    if budget_cost_type is not None:
        request_body["budgetCostType"] = budget_cost_type

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Discount/Fee {discount_fee_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def delete_discount_or_fee(discount_fee_id: str) -> dict:
    """
    Delete a discount or fee from ServiceTitan pricebook.
    
    Args:
        discount_fee_id: The ID of the discount/fee to delete (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/discounts-and-fees/{discount_fee_id}"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Discount/Fee {discount_fee_id} not found"}
        response.raise_for_status()
        return {"success": f"Discount/Fee {discount_fee_id} deleted successfully"}

# IMAGES ENDPOINTS

@mcp.tool()
async def get_images(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Retrieve images from ServiceTitan pricebook.
    
    Args:
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/images"

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
async def upload_image(
    image_data: str,
    file_name: str,
    content_type: Optional[str] = None
) -> dict:
    """
    Upload an image to ServiceTitan pricebook.
    
    Args:
        image_data: Base64 encoded image data (required)
        file_name: Name of the image file (required)
        content_type: MIME type of the image (e.g., 'image/jpeg', 'image/png')
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/images"

    request_body = {
        "imageData": image_data,
        "fileName": file_name
    }

    if content_type is not None:
        request_body["contentType"] = content_type

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

# MATERIALS MARKUP ENDPOINTS

@mcp.tool()
async def get_materials_markup(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Retrieve materials markup configurations from ServiceTitan pricebook.
    
    Args:
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materialsmarkup"

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
async def create_materials_markup(
    name: str,
    markup_percentage: float,
    category_ids: Optional[list] = None,
    vendor_ids: Optional[list] = None,
    active: Optional[bool] = True
) -> dict:
    """
    Create a new materials markup configuration.
    
    Args:
        name: Name of the markup configuration (required)
        markup_percentage: Markup percentage to apply (required)
        category_ids: List of category IDs to apply markup to
        vendor_ids: List of vendor IDs to apply markup to
        active: Whether the markup configuration is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materialsmarkup"

    request_body = {
        "name": name,
        "markupPercentage": markup_percentage
    }

    if category_ids is not None:
        request_body["categoryIds"] = category_ids
    if vendor_ids is not None:
        request_body["vendorIds"] = vendor_ids
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_materials_markup_by_id(markup_id: str) -> dict:
    """
    Retrieve a specific materials markup configuration by ID.
    
    Args:
        markup_id: The ID of the markup configuration to retrieve (required)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materialsmarkup/{markup_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 404:
            return {"error": f"Materials markup {markup_id} not found"}
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_materials_markup(
    markup_id: str,
    name: Optional[str] = None,
    markup_percentage: Optional[float] = None,
    category_ids: Optional[list] = None,
    vendor_ids: Optional[list] = None,
    active: Optional[bool] = None
) -> dict:
    """
    Update an existing materials markup configuration.
    
    Args:
        markup_id: ID of the markup configuration to update (required)
        name: Name of the markup configuration
        markup_percentage: Markup percentage to apply
        category_ids: List of category IDs to apply markup to
        vendor_ids: List of vendor IDs to apply markup to
        active: Whether the markup configuration is active
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/materialsmarkup/{markup_id}"

    request_body = {}

    if name is not None:
        request_body["name"] = name
    if markup_percentage is not None:
        request_body["markupPercentage"] = markup_percentage
    if category_ids is not None:
        request_body["categoryIds"] = category_ids
    if vendor_ids is not None:
        request_body["vendorIds"] = vendor_ids
    if active is not None:
        request_body["active"] = active

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Materials markup {markup_id} not found"}
        response.raise_for_status()
        return response.json()

# CLIENT SPECIFIC PRICING ENDPOINTS

@mcp.tool()
async def get_client_specific_pricing(
    ids: Optional[str] = None,
    search_term: Optional[str] = None,
    active: Optional[str] = None,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False
) -> dict:
    """
    Retrieve client specific pricing rate sheets from ServiceTitan pricebook.
    
    Args:
        ids: Lookup by multiple IDs
        search_term: Search term to filter rate sheets
        active: Filter by active status ("True", "Any", "False")
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/clientspecificpricing"

    params = {
        "ids": ids,
        "searchTerm": search_term,
        "active": active,
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
async def update_client_specific_pricing(
    rate_sheet_id: str,
    exceptions: list
) -> dict:
    """
    Update client specific pricing rate sheet exceptions.
    
    Args:
        rate_sheet_id: ID of the rate sheet to update (required)
        exceptions: List of pricing exceptions with skuId, value, and valueType (required)
                   Example: [{"skuId": 123, "value": 10.0, "valueType": "Percent"}]
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/clientspecificpricing/{rate_sheet_id}"

    request_body = {"exceptions": exceptions}

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        if response.status_code == 404:
            return {"error": f"Rate sheet {rate_sheet_id} not found"}
        response.raise_for_status()
        return response.json()

# EXPORT ENDPOINTS

@mcp.tool()
async def export_categories() -> dict:
    """
    Export categories data from ServiceTitan pricebook.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/export/categories"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_equipment() -> dict:
    """
    Export equipment data from ServiceTitan pricebook.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/export/equipment"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_services() -> dict:
    """
    Export services data from ServiceTitan pricebook.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/export/services"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def export_materials() -> dict:
    """
    Export materials data from ServiceTitan pricebook.
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/export/materials"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

# PRICEBOOK ENDPOINTS

@mcp.tool()
async def create_pricebook_entry(
    sku_type: str,
    sku_id: int,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    business_unit_ids: Optional[list] = None,
    effective_date: Optional[str] = None,
    expiration_date: Optional[str] = None
) -> dict:
    """
    Create a new pricebook entry in ServiceTitan.
    
    Args:
        sku_type: Type of SKU ("Service", "Material", "Equipment", "DiscountFee") (required)
        sku_id: ID of the SKU (required)
        price: Regular price
        member_price: Member price
        add_on_price: Add-on price
        add_on_member_price: Add-on member price
        business_unit_ids: List of business unit IDs
        effective_date: Effective date (RFC3339 format)
        expiration_date: Expiration date (RFC3339 format)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/pricebook"

    request_body = {
        "skuType": sku_type,
        "skuId": sku_id
    }

    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if business_unit_ids is not None:
        request_body["businessUnitIds"] = business_unit_ids
    if effective_date is not None:
        request_body["effectiveDate"] = effective_date
    if expiration_date is not None:
        request_body["expirationDate"] = expiration_date

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def update_pricebook_entry(
    entry_id: str,
    sku_type: Optional[str] = None,
    sku_id: Optional[int] = None,
    price: Optional[float] = None,
    member_price: Optional[float] = None,
    add_on_price: Optional[float] = None,
    add_on_member_price: Optional[float] = None,
    business_unit_ids: Optional[list] = None,
    effective_date: Optional[str] = None,
    expiration_date: Optional[str] = None
) -> dict:
    """
    Update an existing pricebook entry in ServiceTitan.
    
    Args:
        entry_id: ID of the pricebook entry to update (required)
        sku_type: Type of SKU ("Service", "Material", "Equipment", "DiscountFee")
        sku_id: ID of the SKU
        price: Regular price
        member_price: Member price
        add_on_price: Add-on price
        add_on_member_price: Add-on member price
        business_unit_ids: List of business unit IDs
        effective_date: Effective date (RFC3339 format)
        expiration_date: Expiration date (RFC3339 format)
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.servicetitan.io/pricebook/v2/tenant/{TENANT_ID}/pricebook"

    request_body = {}

    if sku_type is not None:
        request_body["skuType"] = sku_type
    if sku_id is not None:
        request_body["skuId"] = sku_id
    if price is not None:
        request_body["price"] = price
    if member_price is not None:
        request_body["memberPrice"] = member_price
    if add_on_price is not None:
        request_body["addOnPrice"] = add_on_price
    if add_on_member_price is not None:
        request_body["addOnMemberPrice"] = add_on_member_price
    if business_unit_ids is not None:
        request_body["businessUnitIds"] = business_unit_ids
    if effective_date is not None:
        request_body["effectiveDate"] = effective_date
    if expiration_date is not None:
        request_body["expirationDate"] = expiration_date

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
