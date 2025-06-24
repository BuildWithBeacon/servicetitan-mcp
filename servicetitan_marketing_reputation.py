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
mcp = FastMCP("ServiceTitan Marketing Reputation")

# Environment variables
CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")
APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID")

# OAuth + API URLs
TOKEN_URL = "https://auth.servicetitan.io/connect/token"
BASE_URL = f"https://api.servicetitan.io/marketingreputation/v2/tenant/{TENANT_ID}"

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
async def get_reviews(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    include_total: Optional[bool] = False,
    search: Optional[str] = None,
    report_type: Optional[int] = None,
    sort: Optional[str] = None,
    created_on_or_after: Optional[str] = None,
    created_before: Optional[str] = None,
    modified_on_or_after: Optional[str] = None,
    modified_before: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    response_types: Optional[str] = None,
    location_ids: Optional[str] = None,
    sources: Optional[str] = None,
    review_statuses: Optional[str] = None,
    technician_ids: Optional[str] = None,
    campaign_ids: Optional[str] = None,
    from_rating: Optional[float] = None,
    to_rating: Optional[float] = None,
    include_reviews_without_location: Optional[bool] = None,
    include_reviews_without_campaign: Optional[bool] = None,
    include_reviews_without_technician: Optional[bool] = None
) -> dict:
    """
    Gets reviews from ServiceTitan Marketing Reputation API.
    
    Args:
        page: The logical number of page to return, starting from 1
        page_size: How many records to return (50 by default)
        include_total: Whether total count should be returned
        search: Search term to filter reviews
        report_type: Report type (0, 1, or 2)
        sort: Applies sorting by field (+FieldName ascending, -FieldName descending)
        created_on_or_after: Return items created on or after certain date/time (RFC3339 format)
        created_before: Return items created before certain date/time (RFC3339 format)
        modified_on_or_after: Return items modified on or after certain date/time (RFC3339 format)
        modified_before: Return items modified before certain date/time (RFC3339 format)
        from_date: Filter reviews from this date (RFC3339 format)
        to_date: Filter reviews to this date (RFC3339 format)
        response_types: Array of response types to filter by
        location_ids: Array of location IDs to filter by
        sources: Array of review sources to filter by
        review_statuses: Array of review statuses to filter by
        technician_ids: Array of technician IDs to filter by
        campaign_ids: Array of campaign IDs to filter by
        from_rating: Minimum rating to filter by (float)
        to_rating: Maximum rating to filter by (float)
        include_reviews_without_location: Include reviews without location
        include_reviews_without_campaign: Include reviews without campaign
        include_reviews_without_technician: Include reviews without technician
    
    Returns:
        dict: JSON response containing review data with fields:
              - address: Review address
              - platform: Review platform
              - authorEmail: Author email
              - authorName: Author name
              - review: Review text
              - reviewType: Review type (0, 1, 2)
              - reviewResponse: Response to review
              - publishDate: Publish date
              - rating: Review rating (float)
              - recommendationStatus: Recommendation status
              - verificationStatus: Verification status
              - jobId: Associated job ID
              - verifiedByUserId: User who verified
              - verifiedOn: Verification date
              - isAutoVerified: Auto verification flag
              - businessUnitId: Business unit ID
              - completedDate: Job completion date
              - customerName: Customer name
              - customerId: Customer ID
              - dispatchedDate: Job dispatch date
              - jobStatus: Job status
              - jobTypeName: Job type name
              - technicianFullName: Technician full name
              - technicianId: Technician ID
    """
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "ST-App-Key": APP_KEY
    }

    url = f"{BASE_URL}/reviews"

    params = {
        "page": page,
        "pageSize": page_size,
        "includeTotal": include_total,
        "search": search,
        "reportType": report_type,
        "sort": sort,
        "createdOnOrAfter": created_on_or_after,
        "createdBefore": created_before,
        "modifiedOnOrAfter": modified_on_or_after,
        "modifiedBefore": modified_before,
        "fromDate": from_date,
        "toDate": to_date,
        "responseTypes": response_types,
        "locationIds": location_ids,
        "sources": sources,
        "reviewStatuses": review_statuses,
        "technicianIds": technician_ids,
        "campaignIds": campaign_ids,
        "fromRating": from_rating,
        "toRating": to_rating,
        "includeReviewsWithoutLocation": include_reviews_without_location,
        "includeReviewsWithoutCampaign": include_reviews_without_campaign,
        "includeReviewsWithoutTechnician": include_reviews_without_technician
    }

    # Remove None values from params
    clean_params_dict = clean_params(params)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=clean_params_dict)
        if response.status_code == 404:
            return {"error": "Reviews not found"}
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio") 