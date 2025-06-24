#!/usr/bin/env python3
"""
ServiceTitan Customer Interactions v2 API MCP Server

This server provides access to ServiceTitan's Customer Interactions v2 API endpoints,
focusing on technician ratings and customer feedback management.

Author: Assistant
Version: 1.0.0
"""

from mcp.server.fastmcp import FastMCP
import os
import httpx
from typing import Optional, Dict, Any, List
import time

# Configuration - Environment variable names match other ServiceTitan files
SERVICETITAN_APP_KEY = os.getenv("SERVICE_TITAN_APP_KEY")
SERVICETITAN_TENANT_ID = os.getenv("SERVICE_TITAN_TENANT_ID") 
SERVICETITAN_CLIENT_ID = os.getenv("SERVICE_TITAN_CLIENT_ID")
SERVICETITAN_CLIENT_SECRET = os.getenv("SERVICE_TITAN_CLIENT_SECRET")

# Validate environment variables on import
if not all([SERVICETITAN_CLIENT_ID, SERVICETITAN_CLIENT_SECRET, SERVICETITAN_APP_KEY, SERVICETITAN_TENANT_ID]):
    missing_vars = []
    if not SERVICETITAN_CLIENT_ID: missing_vars.append("SERVICE_TITAN_CLIENT_ID")
    if not SERVICETITAN_CLIENT_SECRET: missing_vars.append("SERVICE_TITAN_CLIENT_SECRET") 
    if not SERVICETITAN_APP_KEY: missing_vars.append("SERVICE_TITAN_APP_KEY")
    if not SERVICETITAN_TENANT_ID: missing_vars.append("SERVICE_TITAN_TENANT_ID")
    
    # Missing environment variables will be caught later in get_access_token()
    # Don't raise an error on import, just warn

# Base URLs
AUTH_BASE_URL = "https://auth.servicetitan.io"
API_BASE_URL = "https://api.servicetitan.io/customer-interactions/v2"

# Global variables for token management
_access_token = None
_token_expires_at = 0

mcp = FastMCP("servicetitan-customer-interactions")

async def get_access_token() -> str:
    """Get a valid access token, refreshing if necessary."""
    global _access_token, _token_expires_at
    
    # Check environment variables here instead of at module load time
    if not all([SERVICETITAN_CLIENT_ID, SERVICETITAN_CLIENT_SECRET, SERVICETITAN_APP_KEY, SERVICETITAN_TENANT_ID]):
        missing_vars = []
        if not SERVICETITAN_CLIENT_ID: missing_vars.append("SERVICE_TITAN_CLIENT_ID")
        if not SERVICETITAN_CLIENT_SECRET: missing_vars.append("SERVICE_TITAN_CLIENT_SECRET") 
        if not SERVICETITAN_APP_KEY: missing_vars.append("SERVICE_TITAN_APP_KEY")
        if not SERVICETITAN_TENANT_ID: missing_vars.append("SERVICE_TITAN_TENANT_ID")
        error_msg = f"ERROR_ENV: Missing ServiceTitan environment variables: {', '.join(missing_vars)}"
        raise ValueError(error_msg)
    
    if _access_token and time.time() < _token_expires_at:
        return _access_token
    
    async with httpx.AsyncClient() as client:
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": SERVICETITAN_CLIENT_ID,
            "client_secret": SERVICETITAN_CLIENT_SECRET
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
        "ST-App-Key": SERVICETITAN_APP_KEY,
        "Content-Type": "application/json"
    }
    
    url = f"{API_BASE_URL}/tenant/{SERVICETITAN_TENANT_ID}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers, params=params, json=data)
        if response.status_code >= 400:
            error_text = response.text
            raise Exception(f"API request failed: {response.status_code} - {error_text}")
        
        # Handle successful responses that may not have JSON content
        if response.status_code == 200:
            try:
                return response.json()
            except:
                # If no JSON content, return success indicator
                return {"success": True, "status": response.status_code}
        
        return {"success": True, "status": response.status_code}

# TECHNICIAN RATINGS
@mcp.tool()
async def add_or_update_technician_rating(
    technician_id: int,
    job_id: int,
    rating_value: float
) -> Dict[str, Any]:
    """
    Add a rating for the specified technician, tied to the specific job.
    If the rating already exists for that technician/job combination, update it with the new score.
    
    Args:
        technician_id: The ID of the technician to rate
        job_id: The ID of the job associated with this rating
        rating_value: The rating value (typically 0.0 to 5.0)
    
    Returns:
        Dictionary containing the operation result
    """
    data = {"value": rating_value}
    
    endpoint = f"/technician-rating/technician/{technician_id}/job/{job_id}"
    return await make_api_request("PUT", endpoint, data=data)

@mcp.tool()
async def set_technician_rating(
    technician_id: int,
    job_id: int,
    rating_value: float
) -> Dict[str, Any]:
    """
    Set a technician rating for a specific job. This is an alias for add_or_update_technician_rating
    for clearer intent when setting ratings.
    
    Args:
        technician_id: The ID of the technician to rate
        job_id: The ID of the job associated with this rating
        rating_value: The rating value (typically 0.0 to 5.0)
    
    Returns:
        Dictionary containing the operation result
    """
    return await add_or_update_technician_rating(technician_id, job_id, rating_value)

@mcp.tool()
async def update_technician_rating(
    technician_id: int,
    job_id: int,
    rating_value: float
) -> Dict[str, Any]:
    """
    Update an existing technician rating for a specific job. This is an alias for add_or_update_technician_rating
    for clearer intent when updating existing ratings.
    
    Args:
        technician_id: The ID of the technician to rate
        job_id: The ID of the job associated with this rating
        rating_value: The new rating value (typically 0.0 to 5.0)
    
    Returns:
        Dictionary containing the operation result
    """
    return await add_or_update_technician_rating(technician_id, job_id, rating_value)

# HELPER FUNCTIONS FOR RATING MANAGEMENT
@mcp.tool()
async def rate_technician_excellent(
    technician_id: int,
    job_id: int
) -> Dict[str, Any]:
    """
    Rate a technician as excellent (5.0 stars) for a specific job.
    
    Args:
        technician_id: The ID of the technician to rate
        job_id: The ID of the job associated with this rating
    
    Returns:
        Dictionary containing the operation result
    """
    return await add_or_update_technician_rating(technician_id, job_id, 5.0)

@mcp.tool()
async def rate_technician_good(
    technician_id: int,
    job_id: int
) -> Dict[str, Any]:
    """
    Rate a technician as good (4.0 stars) for a specific job.
    
    Args:
        technician_id: The ID of the technician to rate
        job_id: The ID of the job associated with this rating
    
    Returns:
        Dictionary containing the operation result
    """
    return await add_or_update_technician_rating(technician_id, job_id, 4.0)

@mcp.tool()
async def rate_technician_average(
    technician_id: int,
    job_id: int
) -> Dict[str, Any]:
    """
    Rate a technician as average (3.0 stars) for a specific job.
    
    Args:
        technician_id: The ID of the technician to rate
        job_id: The ID of the job associated with this rating
    
    Returns:
        Dictionary containing the operation result
    """
    return await add_or_update_technician_rating(technician_id, job_id, 3.0)

@mcp.tool()
async def rate_technician_poor(
    technician_id: int,
    job_id: int
) -> Dict[str, Any]:
    """
    Rate a technician as poor (2.0 stars) for a specific job.
    
    Args:
        technician_id: The ID of the technician to rate
        job_id: The ID of the job associated with this rating
    
    Returns:
        Dictionary containing the operation result
    """
    return await add_or_update_technician_rating(technician_id, job_id, 2.0)

@mcp.tool()
async def rate_technician_very_poor(
    technician_id: int,
    job_id: int
) -> Dict[str, Any]:
    """
    Rate a technician as very poor (1.0 star) for a specific job.
    
    Args:
        technician_id: The ID of the technician to rate
        job_id: The ID of the job associated with this rating
    
    Returns:
        Dictionary containing the operation result
    """
    return await add_or_update_technician_rating(technician_id, job_id, 1.0)

# BATCH RATING OPERATIONS
@mcp.tool()
async def rate_multiple_technicians(
    ratings: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Rate multiple technicians for their respective jobs in a batch operation.
    
    Args:
        ratings: List of rating objects, each containing:
                - technician_id: The ID of the technician
                - job_id: The ID of the job
                - rating_value: The rating value (0.0 to 5.0)
    
    Returns:
        Dictionary containing batch operation results
    """
    results = []
    errors = []
    
    for rating in ratings:
        try:
            technician_id = rating.get("technician_id")
            job_id = rating.get("job_id")
            rating_value = rating.get("rating_value")
            
            if not all([technician_id, job_id, rating_value is not None]):
                errors.append({
                    "rating": rating,
                    "error": "Missing required fields: technician_id, job_id, or rating_value"
                })
                continue
            
            result = await add_or_update_technician_rating(technician_id, job_id, rating_value)
            results.append({
                "technician_id": technician_id,
                "job_id": job_id,
                "rating_value": rating_value,
                "result": result
            })
            
        except Exception as e:
            errors.append({
                "rating": rating,
                "error": str(e)
            })
    
    return {
        "success_count": len(results),
        "error_count": len(errors),
        "results": results,
        "errors": errors
    }

@mcp.tool()
async def apply_standard_ratings_to_job(
    job_id: int,
    technician_ratings: Dict[int, str]
) -> Dict[str, Any]:
    """
    Apply standard rating levels to multiple technicians for a single job.
    
    Args:
        job_id: The ID of the job
        technician_ratings: Dictionary mapping technician IDs to rating levels
                          Supported levels: "excellent", "good", "average", "poor", "very_poor"
    
    Returns:
        Dictionary containing batch operation results
    """
    rating_map = {
        "excellent": 5.0,
        "good": 4.0,
        "average": 3.0,
        "poor": 2.0,
        "very_poor": 1.0
    }
    
    ratings = []
    for technician_id, rating_level in technician_ratings.items():
        if rating_level.lower() in rating_map:
            ratings.append({
                "technician_id": technician_id,
                "job_id": job_id,
                "rating_value": rating_map[rating_level.lower()]
            })
    
    return await rate_multiple_technicians(ratings)

# Server startup
if __name__ == "__main__":
    mcp.run(transport="stdio") 