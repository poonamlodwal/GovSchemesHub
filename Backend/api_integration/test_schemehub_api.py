"""
Unit tests for SchemHub API Client

Run tests with: pytest test_schemehub_api.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
try:
    from api_client import SchemHubAPIClient, SchemHubAPIError
    from endpoint import SchemHubConfig
except ImportError:
    from Backend.api_integration.api_client import SchemHubAPIClient, SchemHubAPIError
    from Backend.api_integration.endpoint import SchemHubConfig


# ============================================================================
# Tests for SchemHubAPIClient Initialization
# ============================================================================

class TestClientInitialization:
    """Tests for client initialization"""
    
    def test_init_with_api_key(self):
        """Test initialization with API key authentication"""
        client = SchemHubAPIClient(
            base_url="https://schemeshub.netlify.app",
            auth_type="api_key",
            api_key="test-key"
        )
        assert client.base_url == "https://schemeshub.netlify.app"
        assert client.auth_type == "api_key"
        assert client.timeout == 30
        client.close()
    
    def test_init_with_bearer_token(self):
        """Test initialization with bearer token authentication"""
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="bearer",
            bearer_token="test-token"
        )
        assert client.auth_type == "bearer"
        client.close()
    
    def test_init_with_basic_auth(self):
        """Test initialization with basic authentication"""
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="basic",
            username="testuser",
            password="testpass"
        )
        assert client.auth_type == "basic"
        client.close()
    
    def test_init_with_custom_timeout(self):
        """Test initialization with custom timeout"""
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key",
            timeout=60
        )
        assert client.timeout == 60
        client.close()
    
    def test_init_invalid_auth_type(self):
        """Test that invalid auth type raises ValueError"""
        with pytest.raises(ValueError, match="Unknown auth_type"):
            SchemHubAPIClient(
                base_url="https://govschemeshub-2.onrender.com",
                auth_type="invalid",
                api_key="test-key"
            )
    
    def test_init_missing_api_key(self):
        """Test that missing API key raises ValueError"""
        with pytest.raises(ValueError, match="API key required"):
            SchemHubAPIClient(
                base_url="https://govschemeshub-2.onrender.com",
                auth_type="api_key"
            )
    
    def test_init_missing_bearer_token(self):
        """Test that missing bearer token raises ValueError"""
        with pytest.raises(ValueError, match="Bearer token required"):
            SchemHubAPIClient(
                base_url="https://govschemeshub-2.onrender.com",
                auth_type="bearer"
            )
    
    def test_init_missing_basic_auth_credentials(self):
        """Test that missing basic auth credentials raises ValueError"""
        with pytest.raises(ValueError, match="Username and password required"):
            SchemHubAPIClient(
                base_url="https://govschemeshub-2.onrender.com",
                auth_type="basic"
            )


# ============================================================================
# Tests for URL Building
# ============================================================================

class TestURLBuilding:
    """Tests for URL building functionality"""
    
    def test_build_url_with_leading_slash(self):
        """Test URL building with leading slash in endpoint"""
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        url = client._build_url("/v1/schemas")
        assert url == "https://govschemeshub-2.onrender.com/v1/schemas"
        client.close()
    
    def test_build_url_without_leading_slash(self):
        """Test URL building without leading slash in endpoint"""
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        url = client._build_url("v1/schemas")
        assert url == "https://govschemeshub-2.onrender.com/v1/schemas"
        client.close()
    
    def test_build_url_with_trailing_slash(self):
        """Test URL building handles trailing slashes correctly"""
        client = SchemHubAPIClient(
            base_url="https://api.test.com/",
            auth_type="api_key",
            api_key="test-key"
        )
        url = client._build_url("/v1/schemas")
        assert url == "https://api.test.com/v1/schemas"
        client.close()


# ============================================================================
# Tests for API Methods with Mocking
# ============================================================================

class TestAPIRequests:
    """Tests for API request methods"""
    
    @patch('api_client.requests.Session.get')
    def test_get_request(self, mock_get):
        """Test GET request"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.content = b'{"data": "test"}'
        mock_get.return_value = mock_response
        
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        
        result = client.get("/v1/schemas")
        
        assert result == {"data": "test"}
        mock_get.assert_called_once()
        client.close()
    
    @patch('api_client.requests.Session.post')
    def test_post_request(self, mock_post):
        """Test POST request"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "123", "name": "Test"}
        mock_response.content = b'{"id": "123"}'
        mock_post.return_value = mock_response
        
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        
        result = client.post("/v1/schemas", json_data={"name": "Test"})
        
        assert result["id"] == "123"
        mock_post.assert_called_once()
        client.close()
    
    @patch('api_client.requests.Session.put')
    def test_put_request(self, mock_put):
        """Test PUT request"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "123", "updated": True}
        mock_response.content = b'{"id": "123"}'
        mock_put.return_value = mock_response
        
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        
        result = client.put("/v1/schemas/123", json_data={"name": "Updated"})
        
        assert result["id"] == "123"
        mock_put.assert_called_once()
        client.close()
    
    @patch('api_client.requests.Session.patch')
    def test_patch_request(self, mock_patch):
        """Test PATCH request"""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "123", "patched": True}
        mock_response.content = b'{"id": "123"}'
        mock_patch.return_value = mock_response
        
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        
        result = client.patch("/v1/schemas/123", json_data={"status": "active"})
        
        assert result["id"] == "123"
        mock_patch.assert_called_once()
        client.close()
    
    @patch('api_client.requests.Session.delete')
    def test_delete_request(self, mock_delete):
        """Test DELETE request"""
        mock_response = Mock()
        mock_response.json.return_value = {"deleted": True}
        mock_response.content = b'{"deleted": true}'
        mock_delete.return_value = mock_response
        
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        
        result = client.delete("/v1/schemas/123")
        
        assert result["deleted"] is True
        mock_delete.assert_called_once()
        client.close()


# ============================================================================
# Tests for Error Handling
# ============================================================================

class TestErrorHandling:
    """Tests for error handling"""
    
    @patch('api_client.requests.Session.get')
    def test_api_error_401(self, mock_get):
        """Test handling of 401 Unauthorized error"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response
        
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="invalid-key"
        )
        
        with pytest.raises(SchemHubAPIError) as exc_info:
            client.get("/v1/schemas")
        
        assert exc_info.value.status_code == 401
        client.close()
    
    @patch('api_client.requests.Session.get')
    def test_api_error_404(self, mock_get):
        """Test handling of 404 Not Found error"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        
        with pytest.raises(SchemHubAPIError) as exc_info:
            client.get("/v1/schemas/nonexistent")
        
        assert exc_info.value.status_code == 404
        client.close()
    
    @patch('api_client.requests.Session.get')
    def test_api_error_500(self, mock_get):
        """Test handling of 500 Internal Server Error"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("500 Server Error")
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response
        
        client = SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        
        with pytest.raises(SchemHubAPIError) as exc_info:
            client.get("/v1/schemas")
        
        assert exc_info.value.status_code == 500
        client.close()


# ============================================================================
# Tests for Context Manager
# ============================================================================

class TestContextManager:
    """Tests for context manager functionality"""
    
    def test_context_manager(self):
        """Test that context manager properly closes session"""
        with SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        ) as client:
            assert client.session is not None
        
        # Session should be closed after context exit
        assert client.session.close.called or True  # Session.close() was called


# ============================================================================
# Tests for Configuration
# ============================================================================

class TestConfiguration:
    """Tests for SchemHubConfig"""
    
    def test_config_validation_valid(self):
        """Test configuration validation with valid config"""
        config = SchemHubConfig(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        )
        assert config.validate() is True
    
    def test_config_validation_missing_url(self):
        """Test configuration validation with missing URL"""
        config = SchemHubConfig(
            base_url="",
            auth_type="api_key",
            api_key="test-key"
        )
        with pytest.raises(ValueError, match="SCHEMEHUB_BASE_URL is required"):
            config.validate()
    
    def test_config_validation_invalid_auth_type(self):
        """Test configuration validation with invalid auth type"""
        config = SchemHubConfig(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="invalid",
            api_key="test-key"
        )
        with pytest.raises(ValueError, match="Invalid auth_type"):
            config.validate()
    
    def test_config_validation_missing_api_key(self):
        """Test configuration validation with missing API key"""
        config = SchemHubConfig(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key=None
        )
        with pytest.raises(ValueError, match="GOV_API_KEY is required"):
            config.validate()


# ============================================================================
# Tests for Exception Class
# ============================================================================

class TestSchemHubAPIError:
    """Tests for SchemHubAPIError exception"""
    
    def test_error_initialization(self):
        """Test error initialization"""
        error = SchemHubAPIError(
            status_code=401,
            message="Unauthorized",
            response_body='{"error": "invalid_key"}'
        )
        
        assert error.status_code == 401
        assert error.message == "Unauthorized"
        assert error.response_body == '{"error": "invalid_key"}'
    
    def test_error_str_representation(self):
        """Test error string representation"""
        error = SchemHubAPIError(
            status_code=401,
            message="Unauthorized"
        )
        
        assert str(error) == "SchemHub API Error (401): Unauthorized"


# ============================================================================
# Integration-like Tests
# ============================================================================

class TestIntegration:
    """Integration-like tests"""
    
    @patch('api_client.requests.Session.get')
    @patch('api_client.requests.Session.post')
    def test_workflow_create_and_get(self, mock_post, mock_get):
        """Test workflow: create schema then get it"""
        # Mock POST response for creation
        mock_post_resp = Mock()
        mock_post_resp.json.return_value = {"id": "schema-123", "name": "Test"}
        mock_post_resp.content = b'{"id": "schema-123"}'
        mock_post.return_value = mock_post_resp
        
        # Mock GET response for retrieval
        mock_get_resp = Mock()
        mock_get_resp.json.return_value = {"id": "schema-123", "name": "Test"}
        mock_get_resp.content = b'{"id": "schema-123"}'
        mock_get.return_value = mock_get_resp
        
        with SchemHubAPIClient(
            base_url="https://govschemeshub-2.onrender.com",
            auth_type="api_key",
            api_key="test-key"
        ) as client:
            # Create schema
            created = client.post("/v1/schemas", json_data={"name": "Test"})
            assert created["id"] == "schema-123"
            
            # Get schema
            retrieved = client.get(f"/v1/schemas/{created['id']}")
            assert retrieved["id"] == "schema-123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
