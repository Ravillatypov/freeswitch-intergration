def is_number(num: str) -> bool:
    return num.isdigit()


def is_internal(num: str) -> bool:
    return num.isdigit() and len(num) < 5


def is_external(num: str) -> bool:
    return num.isdigit() and len(num) > 4
