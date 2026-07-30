import requests
import logging
from typing import Optional, Dict, Any
from requests.auth import HTTPBasicAuth, AuthBase
from urllib.parse import urljoin
import json

# Custom HTTPBearerAuth helper since requests.auth does not export HTTPBearerAuth
class HTTPBearerAuth(AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchemHubAPIError(Exception):
    """Custom exception for SchemHub API errors"""
    def __init__(self, status_code: int, message: str, response_body: Optional[str] = None):
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(self.message)

    def __str__(self):
        return f"SchemHub API Error ({self.status_code}): {self.message}"


class SchemHubAPIClient:
    """
    Python REST API client for SchemHub with authentication support.
    
    Supports multiple authentication methods:
    - API Key (header-based)
    - Bearer Token
    - Basic Authentication
    """
    
    def __init__(
        self,
        base_url: str,
        auth_type: str = "api_key",
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        bearer_token: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize the SchemHub API client.
        
        Args:
            base_url: Base URL of the SchemHub API (e.g., 'https://api.schemehub.com')
            auth_type: Type of authentication ('api_key', 'basic', 'bearer')
            api_key: API key for header-based authentication
            username: Username for basic authentication
            password: Password for basic authentication
            bearer_token: Bearer token for token-based authentication
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.auth_type = auth_type.lower()
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        self.session = requests.Session()
        self._configure_auth(api_key, username, password, bearer_token)
        
        logger.info(f"SchemHub API Client initialized with auth_type: {auth_type}")

    def _configure_auth(
        self,
        api_key: Optional[str],
        username: Optional[str],
        password: Optional[str],
        bearer_token: Optional[str]
    ):
        """Configure authentication for the session."""
        if self.auth_type == "api_key":
            if not api_key:
                raise ValueError("API key required for 'api_key' authentication")
            self.session.headers.update({"X-API-Key": api_key})
            logger.info("API Key authentication configured")
            
        elif self.auth_type == "bearer":
            if not bearer_token:
                raise ValueError("Bearer token required for 'bearer' authentication")
            self.session.auth = HTTPBearerAuth(bearer_token)
            logger.info("Bearer token authentication configured")
            
        elif self.auth_type == "basic":
            if not username or not password:
                raise ValueError("Username and password required for 'basic' authentication")
            self.session.auth = HTTPBasicAuth(username, password)
            logger.info("Basic authentication configured")
            
        else:
            raise ValueError(f"Unknown auth_type: {self.auth_type}")

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return urljoin(self.base_url, endpoint.lstrip('/'))

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise errors for non-2xx status codes.
        
        Args:
            response: Response object from requests library
            
        Returns:
            Parsed JSON response
            
        Raises:
            SchemHubAPIError: For API errors
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_body = response.text
            logger.error(f"API Error {response.status_code}: {error_body}")
            raise SchemHubAPIError(
                status_code=response.status_code,
                message=str(e),
                response_body=error_body
            )
        
        # Handle empty responses
        if not response.content:
            return {}
        
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"raw_response": response.text}

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Parsed JSON response
        """
        url = self._build_url(endpoint)
        merged_headers = self.session.headers.copy()
        if headers:
            merged_headers.update(headers)
        
        logger.info(f"GET {url}")
        response = self.session.get(
            url,
            params=params,
            headers=merged_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        return self._handle_response(response)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: API endpoint path
            data: Form data
            json_data: JSON data to send
            headers: Additional headers
            
        Returns:
            Parsed JSON response
        """
        url = self._build_url(endpoint)
        merged_headers = self.session.headers.copy()
        if headers:
            merged_headers.update(headers)
        
        logger.info(f"POST {url}")
        response = self.session.post(
            url,
            data=data,
            json=json_data,
            headers=merged_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        return self._handle_response(response)

    def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a PUT request to the API.
        
        Args:
            endpoint: API endpoint path
            json_data: JSON data to send
            headers: Additional headers
            
        Returns:
            Parsed JSON response
        """
        url = self._build_url(endpoint)
        merged_headers = self.session.headers.copy()
        if headers:
            merged_headers.update(headers)
        
        logger.info(f"PUT {url}")
        response = self.session.put(
            url,
            json=json_data,
            headers=merged_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        return self._handle_response(response)

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint: API endpoint path
            headers: Additional headers
            
        Returns:
            Parsed JSON response
        """
        url = self._build_url(endpoint)
        merged_headers = self.session.headers.copy()
        if headers:
            merged_headers.update(headers)
        
        logger.info(f"DELETE {url}")
        response = self.session.delete(
            url,
            headers=merged_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        return self._handle_response(response)

    def patch(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a PATCH request to the API.
        
        Args:
            endpoint: API endpoint path
            json_data: JSON data to send
            headers: Additional headers
            
        Returns:
            Parsed JSON response
        """
        url = self._build_url(endpoint)
        merged_headers = self.session.headers.copy()
        if headers:
            merged_headers.update(headers)
        
        logger.info(f"PATCH {url}")
        response = self.session.patch(
            url,
            json=json_data,
            headers=merged_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )
        
        return self._handle_response(response)

    def close(self):
        """Close the session."""
        self.session.close()
        logger.info("API Client session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
