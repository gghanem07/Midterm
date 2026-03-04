########################
# Custom Exceptions    #
########################

class OperationError(Exception):
    """
    Raised when a mathematical operation fails.
    """
    pass


class ValidationError(Exception):
    """
    Raised when input validation fails.
    """
    pass