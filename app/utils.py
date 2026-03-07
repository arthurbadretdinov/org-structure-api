from app.exceptions import ErrorCodeException


def validate_name(name: str, field_name: str, max_length: int = 200) -> str:
    name = name.strip()
    if not name:
        raise ErrorCodeException(
            422, 
            f"{field_name} cannot be empty or whitespace")
    if len(name) > 200:
        raise ErrorCodeException(
            422, 
            f"{field_name} cannot be longer than 200 characters"
            )
    return name