import re

INDEX_NAME_REGEX = re.compile(r"^[A-Za-z0-9_]+$")

# Validation for the INDEX_NAME
def validate_index_name(index_name):
    if index_name is None or not index_name:
        return "index_name is required"
    if not INDEX_NAME_REGEX.fullmatch(index_name):
        return "Invalid index_name: Only letters, numbers, and underscores are allowed"
    return None


# Validation for DIMENSIONS
def validate_dimension(dimension):
    if dimension is None:
        return "dimension is required"
    if isinstance(dimension, bool) or not isinstance(dimension, int):
        return "dimension must be an integer"
    if dimension <= 0:
        return "dimension must be a positive integer"
    return None


# Validating the TOP_K Data Chunks
def validate_top_k(top_k, max_k=512):
    if (
        isinstance(top_k, bool)
        or not isinstance(top_k, int)
        or top_k <= 0
        or top_k > max_k
    ):
        return f"top_k must be an integer between 1 and {max_k}"
    return None


# Validating the EMBEDDED VECTORS
def validate_vector(vector):
    if not isinstance(vector, list) or not vector:
        return "vector must be a non-empty list"
    if not all(isinstance(x, (int, float)) for x in vector):
        return "vector must contain only numbers"
    return None


# For validating the SPACE_TYPES and PRECISIONS
def validate_choice(field_name, allowed):
    if field_name not in allowed:
        return f"{field_name} must be one of {sorted(allowed)}"
    return None