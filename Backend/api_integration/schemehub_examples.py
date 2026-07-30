"""
SchemHub API Client - Usage Examples

This module demonstrates various ways to use the SchemHub API client
with different authentication methods and API operations.
"""

from Backend.api_integration.api_client import SchemHubAPIClient, SchemHubAPIError
from Backend.api_integration.endpoint import SchemHubConfig


# ============================================================================
# Example 1: API Key Authentication
# ============================================================================

def example_api_key_auth():
    """Example using API Key authentication"""
    print("\n=== Example 1: API Key Authentication ===\n")
    
    client = SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="Gov_API_KEY"
    )
    
    try:
        # Get user profile
        profile = client.get("/v1/profile")
        print(f"Profile: {profile}")
        
        # Get list of schemas
        schemas = client.get("/v1/schemas", params={"limit": 10})
        print(f"Schemas: {schemas}")
        
    except SchemHubAPIError as e:
        print(f"Error: {e}")
    finally:
        client.close()


# ============================================================================
# Example 2: Bearer Token Authentication
# ============================================================================

def example_bearer_token_auth():
    """Example using Bearer Token authentication"""
    print("\n=== Example 2: Bearer Token Authentication ===\n")
    
    client = SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="bearer",
        bearer_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    
    try:
        # Authenticate and get token info
        token_info = client.get("/v1/auth/token-info")
        print(f"Token Info: {token_info}")
        
    except SchemHubAPIError as e:
        print(f"Error: {e}")
    finally:
        client.close()


# ============================================================================
# Example 3: Basic Authentication
# ============================================================================

def example_basic_auth():
    """Example using Basic authentication"""
    print("\n=== Example 3: Basic Authentication ===\n")
    
    client = SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="basic",
        username="user@example.com",
        password="password123"
    )
    
    try:
        # Get authenticated user info
        user = client.get("/v1/user")
        print(f"User: {user}")
        
    except SchemHubAPIError as e:
        print(f"Error: {e}")
    finally:
        client.close()


# ============================================================================
# Example 4: Configuration from Environment
# ============================================================================

def example_config_from_env():
    """Example using configuration from environment variables"""
    print("\n=== Example 4: Configuration from Environment ===\n")
    
    # Load configuration from environment variables
    config = SchemHubConfig.from_env()
    
    client = SchemHubAPIClient(
        base_url=config.base_url,
        auth_type=config.auth_type,
        api_key=config.api_key,
        username=config.username,
        password=config.password,
        bearer_token=config.bearer_token,
        timeout=config.timeout,
        verify_ssl=config.verify_ssl
    )
    
    try:
        # Get profile
        profile = client.get("/v1/profile")
        print(f"Profile: {profile}")
        
    except SchemHubAPIError as e:
        print(f"Error: {e}")
    finally:
        client.close()


# ============================================================================
# Example 5: Context Manager (Recommended)
# ============================================================================

def example_context_manager():
    """Example using context manager for automatic cleanup"""
    print("\n=== Example 5: Context Manager ===\n")
    
    # Context manager automatically closes the session
    with SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="Gov_API_KEY"
    ) as client:
        try:
            # Perform API operations
            schemas = client.get("/v1/schemas")
            print(f"Total schemas: {len(schemas.get('data', []))}")
            
        except SchemHubAPIError as e:
            print(f"Error: {e}")


# ============================================================================
# Example 6: Creating a Schema (POST request)
# ============================================================================

def example_create_schema():
    """Example creating a new schema"""
    print("\n=== Example 6: Create Schema ===\n")
    
    with SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="Gov_API_KEY"
    ) as client:
        try:
            schema_data = {
                "name": "User Schema",
                "description": "Schema for user objects",
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string", "format": "email"},
                    "name": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"}
                },
                "required": ["id", "email", "name"]
            }
            
            response = client.post("/v1/schemas", json_data=schema_data)
            schema_id = response.get("id")
            print(f"Schema created with ID: {schema_id}")
            print(f"Response: {response}")
            
        except SchemHubAPIError as e:
            print(f"Error: {e}")


# ============================================================================
# Example 7: Updating a Schema (PUT request)
# ============================================================================

def example_update_schema(schema_id: str):
    """Example updating an existing schema"""
    print(f"\n=== Example 7: Update Schema {schema_id} ===\n")
    
    with SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="Gov_API_KEY"
    ) as client:
        try:
            updated_data = {
                "description": "Updated schema for user objects",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string", "format": "email"},
                    "name": {"type": "string"},
                    "phone": {"type": "string"},  # New field
                    "created_at": {"type": "string", "format": "date-time"}
                }
            }
            
            response = client.put(f"/v1/schemas/{schema_id}", json_data=updated_data)
            print(f"Schema updated successfully")
            print(f"Response: {response}")
            
        except SchemHubAPIError as e:
            print(f"Error: {e}")


# ============================================================================
# Example 8: Partially Update a Schema (PATCH request)
# ============================================================================

def example_patch_schema(schema_id: str):
    """Example partially updating a schema"""
    print(f"\n=== Example 8: Patch Schema {schema_id} ===\n")
    
    with SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="GoV_API_KEY"
    ) as client:
        try:
            patch_data = {
                "description": "Partially updated description"
            }
            
            response = client.patch(f"/v1/schemas/{schema_id}", json_data=patch_data)
            print(f"Schema patched successfully")
            print(f"Response: {response}")
            
        except SchemHubAPIError as e:
            print(f"Error: {e}")


# ============================================================================
# Example 9: Delete a Schema (DELETE request)
# ============================================================================

def example_delete_schema(schema_id: str):
    """Example deleting a schema"""
    print(f"\n=== Example 9: Delete Schema {schema_id} ===\n")
    
    with SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="Gov_API_KEY"
    ) as client:
        try:
            response = client.delete(f"/v1/schemas/{schema_id}")
            print(f"Schema deleted successfully")
            print(f"Response: {response}")
            
        except SchemHubAPIError as e:
            print(f"Error: {e}")


# ============================================================================
# Example 10: Error Handling
# ============================================================================

def example_error_handling():
    """Example demonstrating error handling"""
    print("\n=== Example 10: Error Handling ===\n")
    
    with SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="invalid-api-key"
    ) as client:
        try:
            # This will likely fail due to invalid API key
            response = client.get("/v1/schemas")
            
        except SchemHubAPIError as e:
            print(f"Caught API Error:")
            print(f"  Status Code: {e.status_code}")
            print(f"  Message: {e.message}")
            print(f"  Response Body: {e.response_body}")
        except Exception as e:
            print(f"Caught unexpected error: {type(e).__name__}: {e}")


# ============================================================================
# Example 11: Paginated Requests
# ============================================================================

def example_paginated_requests():
    """Example handling paginated API responses"""
    print("\n=== Example 11: Paginated Requests ===\n")
    
    with SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="Gov_API_KEY"
    ) as client:
        try:
            page = 1
            all_schemas = []
            
            while True:
                response = client.get(
                    "/v1/schemas",
                    params={"page": page, "limit": 20}
                )
                
                schemas = response.get("data", [])
                if not schemas:
                    break
                
                all_schemas.extend(schemas)
                
                # Check if there are more pages
                if not response.get("has_next", False):
                    break
                
                page += 1
            
            print(f"Total schemas retrieved: {len(all_schemas)}")
            
        except SchemHubAPIError as e:
            print(f"Error: {e}")


# ============================================================================
# Example 12: Custom Headers
# ============================================================================

def example_custom_headers():
    """Example adding custom headers to requests"""
    print("\n=== Example 12: Custom Headers ===\n")
    
    with SchemHubAPIClient(
        base_url="https://schemeshub.netlify.app",
        auth_type="api_key",
        api_key="Gov_API_KEY"
    ) as client:
        try:
            custom_headers = {
                "X-Request-ID": "unique-request-id-123",
                "X-Custom-Header": "custom-value"
            }
            
            response = client.get(
                "/v1/schemas",
                headers=custom_headers
            )
            print(f"Response: {response}")
            
        except SchemHubAPIError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Run examples (comment out or modify as needed)
    print("SchemHub API Client - Usage Examples")
    print("=" * 50)
    
    # Uncomment the example you want to run:
    # example_api_key_auth()
    # example_bearer_token_auth()
    # example_basic_auth()
    # example_config_from_env()
    # example_context_manager()
    # example_create_schema()
    # example_update_schema("schema-id-here")
    # example_patch_schema("schema-id-here")
    # example_delete_schema("schema-id-here")
    # example_error_handling()
    # example_paginated_requests()
    # example_custom_headers()
    
    print("\nNote: Update the base URL and credentials before running examples.")
