class APIError(Exception):
    """Base exception for API related errors."""
    pass

class APIKeyError(APIError):
    """Exception raised for API key related errors."""
    pass

class ModelError(APIError):
    """Exception raised for model related errors."""
    pass

class ProviderError(APIError):
    """Exception raised for provider related errors."""
    pass

class ValidationError(APIError):
    """Exception raised for input validation errors."""
    pass

def handle_api_error(error: APIError) -> dict:
    """Convert API errors to response dictionaries."""
    error_types = {
        APIKeyError: (400, "API Key Error"),
        ModelError: (400, "Model Error"),
        ProviderError: (500, "Provider Error"),
        ValidationError: (400, "Validation Error"),
        APIError: (500, "Internal Server Error")
    }
    
    error_class = type(error)
    status_code, error_type = error_types.get(error_class, (500, "Unknown Error"))
    
    return {
        "status_code": status_code,
        "error_type": error_type,
        "detail": str(error)
    }