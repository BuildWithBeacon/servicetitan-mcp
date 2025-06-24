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
BASE_URL = f"https://api.servicetitan.io/marketingads/v2/tenant/{TENANT_ID}"

# FastMCP instance for Marketing Ads ServiceTitan API
mcp = FastMCP("servicetitan-marketing-ads")

async def get_access_token() -> str:
    """Fetch OAuth2 access token from ServiceTitan."""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("CLIENT_ID and CLIENT_SECRET must be set")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get access token: {response.status_code}")
        
        return response.json()["access_token"]

def clean_params(params: dict) -> dict:
    """Remove None values from parameters."""
    return {k: v for k, v in params.items() if v is not None}

async def make_request(method: str, endpoint: str, params: dict = None, json_data: dict = None):
    """Make authenticated request to ServiceTitan Marketing Ads API."""
    try:
        token = await get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "ST-App-Key": APP_KEY,
            "Content-Type": "application/json"
        }
        
        url = f"{BASE_URL}{endpoint}"
        cleaned_params = clean_params(params) if params else None
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=headers, params=cleaned_params)
            elif method == "POST":
                response = await client.post(url, headers=headers, params=cleaned_params, json=json_data)
            elif method == "PATCH":
                response = await client.patch(url, headers=headers, params=cleaned_params, json=json_data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {
                "error": f"HTTP {response.status_code}",
                "message": response.text
            }
    
    except Exception as e:
        return {
            "error": "Request failed",
            "message": str(e)
        }

# ============================================================================
# ATTRIBUTED LEADS ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_attributed_leads(
    from_utc: str,
    to_utc: str,
    lead_type: Optional[str] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None
) -> dict:
    """
    Retrieve attributed leads data with filtering and pagination.

    Args:
        from_utc: Start date and time in UTC for filtering period (required, RFC3339 format)
        to_utc: End date and time in UTC for filtering period (required, RFC3339 format)
        lead_type: Type of lead for filtering (Call, WebBooking, WebLeadForm, ManualJob)
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned

    Returns:
        Paginated response with attributed leads data including attribution details,
        job info, customer info, call details, lead forms, and bookings.
    """
    params = {
        "fromUtc": from_utc,
        "toUtc": to_utc,
        "leadType": lead_type,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }
    
    return await make_request("GET", "/attributed-leads", params)

# ============================================================================
# CAPACITY WARNINGS ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_capacity_warnings() -> dict:
    """
    Retrieve all capacity awareness warnings.

    Returns:
        Response containing tenant info and list of capacity warnings with
        campaign names, warning types, business units, lookahead windows, and thresholds.
    """
    return await make_request("GET", "/capacity-warnings")

# ============================================================================
# PERFORMANCE DATA ENDPOINTS
# ============================================================================

@mcp.tool()
async def get_performance_data(
    from_utc: str,
    to_utc: str,
    performance_segmentation_type: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_total: Optional[bool] = None
) -> dict:
    """
    Retrieve marketing performance data with segmentation.

    Args:
        from_utc: Start date and time in UTC for filtering period (required, RFC3339 format)
        to_utc: End date and time in UTC for filtering period (required, RFC3339 format)
        performance_segmentation_type: Type of performance segmentation (Campaign, AdGroup, Keyword)
        page: Page number to return (starting from 1)
        page_size: Number of records to return (50 by default)
        include_total: Whether total count should be returned

    Returns:
        Paginated response with performance data including campaign, ad group, keyword info,
        digital stats (impressions, clicks, conversions), lead stats, and ROI.
    """
    params = {
        "fromUtc": from_utc,
        "toUtc": to_utc,
        "performanceSegmentationType": performance_segmentation_type,
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total
    }
    
    return await make_request("GET", "/performance", params)

# ============================================================================
# ATTRIBUTION ENDPOINTS
# ============================================================================

@mcp.tool()
async def attribute_external_call(
    web_session_data: dict,
    external_call_data: dict
) -> dict:
    """
    Attribute an external call (from Call Tracking Software) to a web session.

    Args:
        web_session_data: Web session information containing:
            - landingPageUrl: Landing page URL
            - referrerUrl: Referrer URL
            - gclid: Google Click ID
            - gbraid: Google enhanced conversions identifier
            - wbraid: Google enhanced conversions identifier
            - fbclid: Facebook Click ID
            - msclkid: Microsoft Click ID
            - utmSource: UTM source parameter
            - utmMedium: UTM medium parameter
            - utmCampaign: UTM campaign parameter
            - utmAdgroup: UTM ad group parameter
            - utmTerm: UTM term parameter
            - utmContent: UTM content parameter
            - googleAnalyticsClientId: Google Analytics client ID
        external_call_data: External call information containing:
            - customerPhoneNumber: Customer's phone number
            - forwardingPhoneNumber: Forwarding phone number
            - trackingPhoneNumber: Tracking phone number
            - callStartedOnUtc: Call start time in UTC (RFC3339 format)

    Returns:
        Success confirmation or error details.
    """
    json_data = {
        "webSessionData": web_session_data,
        "externalCallData": external_call_data
    }
    
    return await make_request("POST", "/external-call-attributions", json_data=json_data)

@mcp.tool()
async def attribute_job(
    web_session_data: dict,
    job_id: int
) -> dict:
    """
    Attribute a job to a web session.

    Args:
        web_session_data: Web session information containing:
            - landingPageUrl: Landing page URL
            - referrerUrl: Referrer URL
            - gclid: Google Click ID
            - gbraid: Google enhanced conversions identifier
            - wbraid: Google enhanced conversions identifier
            - fbclid: Facebook Click ID
            - msclkid: Microsoft Click ID
            - utmSource: UTM source parameter
            - utmMedium: UTM medium parameter
            - utmCampaign: UTM campaign parameter
            - utmAdgroup: UTM ad group parameter
            - utmTerm: UTM term parameter
            - utmContent: UTM content parameter
            - googleAnalyticsClientId: Google Analytics client ID
        job_id: ID of the job to attribute

    Returns:
        Success confirmation or error details.
    """
    json_data = {
        "webSessionData": web_session_data,
        "jobId": job_id
    }
    
    return await make_request("POST", "/job-attributions", json_data=json_data)

@mcp.tool()
async def attribute_web_booking(
    web_session_data: dict,
    booking_id: int
) -> dict:
    """
    Attribute a web booking to a web session.

    Args:
        web_session_data: Web session information containing:
            - landingPageUrl: Landing page URL
            - referrerUrl: Referrer URL
            - gclid: Google Click ID
            - gbraid: Google enhanced conversions identifier
            - wbraid: Google enhanced conversions identifier
            - fbclid: Facebook Click ID
            - msclkid: Microsoft Click ID
            - utmSource: UTM source parameter
            - utmMedium: UTM medium parameter
            - utmCampaign: UTM campaign parameter
            - utmAdgroup: UTM ad group parameter
            - utmTerm: UTM term parameter
            - utmContent: UTM content parameter
            - googleAnalyticsClientId: Google Analytics client ID
        booking_id: ID of the booking to attribute

    Returns:
        Success confirmation or error details.
    """
    json_data = {
        "webSessionData": web_session_data,
        "bookingId": booking_id
    }
    
    return await make_request("POST", "/web-booking-attributions", json_data=json_data)

@mcp.tool()
async def attribute_web_lead_form(
    web_session_data: dict,
    lead_id: int
) -> dict:
    """
    Attribute a web lead form to a web session.

    Args:
        web_session_data: Web session information containing:
            - landingPageUrl: Landing page URL
            - referrerUrl: Referrer URL
            - gclid: Google Click ID
            - gbraid: Google enhanced conversions identifier
            - wbraid: Google enhanced conversions identifier
            - fbclid: Facebook Click ID
            - msclkid: Microsoft Click ID
            - utmSource: UTM source parameter
            - utmMedium: UTM medium parameter
            - utmCampaign: UTM campaign parameter
            - utmAdgroup: UTM ad group parameter
            - utmTerm: UTM term parameter
            - utmContent: UTM content parameter
            - googleAnalyticsClientId: Google Analytics client ID
        lead_id: ID of the lead to attribute

    Returns:
        Success confirmation or error details.
    """
    json_data = {
        "webSessionData": web_session_data,
        "leadId": lead_id
    }
    
    return await make_request("POST", "/web-lead-form-attributions", json_data=json_data)

if __name__ == "__main__":
    mcp.run(transport="stdio") 