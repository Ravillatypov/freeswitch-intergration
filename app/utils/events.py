import uuid


def is_number(num: str) -> bool:
    return num.isdigit()


def is_internal(num: str) -> bool:
    return num.isdigit() and len(num) < 5


def is_external(num: str) -> bool:
    return num.isdigit() and len(num) > 4


def is_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
    except Exception:
        return False
    else:
        return True
