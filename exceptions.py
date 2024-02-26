class ScaleSafeException(Exception):
    """Base exception class for ScaleSafe errors."""
    pass

class ScaleSafeTokenError(Exception):
    """Something looks wrong with your ScaleSafe API Key. Have a look inside your object's api_key variable or on your account at app.scalesafe.ai."""
    pass

class OutOfComplianceError(ScaleSafeException):
    """Exception raised when an operation violates compliance rules."""
    pass

class HumanStoppedTheLoopError(OutOfComplianceError):
    """Exception raised when a human intervention stops a loop or process."""
    pass

class UnsafeInputError(OutOfComplianceError):
    """Exception raised for inputs deemed unsafe or risky."""
    pass

class BannedOutputError(OutOfComplianceError):
    """Exception raised when an output is banned or not allowed."""
    pass

class BannedLocationError(OutOfComplianceError):
    """Exception raised when a location is banned or not allowed for operations."""
    pass

class ConfigurationError(OutOfComplianceError):
    """Exception raised for issues related to configuration settings."""
    pass

class HumanReviewNeededException(ScaleSafeException):
    """Exception raised when human review is needed for a process."""
    pass