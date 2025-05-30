class SimulationError(Exception):
    """Base exception for all simulation errors."""
    pass

class NavigationError(SimulationError):
    """Raised when there are issues navigating the website."""
    pass

class FormError(SimulationError):
    """Raised when there are issues with form filling."""
    pass

class TimeoutError(SimulationError):
    """Raised when a simulation times out."""
    pass

class ValidationError(SimulationError):
    """Raised when input validation fails."""
    pass

class CacheError(SimulationError):
    """Raised when there are issues with cache operations."""
    pass

class RateLimitError(SimulationError):
    """Raised when rate limit is exceeded."""
    pass

class DataGenerationError(SimulationError):
    """Raised when there are issues generating random data."""
    pass

class ResponseFormatError(SimulationError):
    """Raised when there are issues formatting the response."""
    pass 