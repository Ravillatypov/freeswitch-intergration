import uuid
import re


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


def phone_number_normalize(phone_number: str) -> str:
    phone_number = re.sub(r"[\+() ]", "", phone_number)
    phone_number = phone_number.replace('sip:', '').split('@')[0]

    # standard phone num normalization
    phone_regex = re.compile(r'([7,8])(\d{10})')
    pieces = phone_regex.split(phone_number)
    if len(pieces) > 1:
        return '7' + pieces[2]

    standard_num = ''.join((i for i in phone_number if i.isdigit()))
    if re.match(r"\d{11}", standard_num):
        phone_number = standard_num

    m = re.search(r'\d{7,11}', phone_number)
    if m is not None:
        phone_number = m.group()

    return phone_number

