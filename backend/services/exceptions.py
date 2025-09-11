class ServiceError(Exception):
    """Base class for all service-level errors."""

class AgentInitError(ServiceError):
    """Raised when the LLM agent cannot be initialized."""

class LLMCallError(ServiceError):
    """Raised when the LLM call fails."""

class JobParseError(ServiceError):
    """Raised when parsing a job description fails."""