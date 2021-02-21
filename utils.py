from datetime import datetime

def to_bool(value: str) -> bool:
    return True if value == '1' else False

def to_int(value: str) -> int:
    return int(value) if value else 0

def to_datetime(value: str) -> datetime:
    if not value:
        return None

    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None