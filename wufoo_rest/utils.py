from datetime import datetime
from typing import Optional, Dict


def to_bool(value: str) -> bool:
    return True if value == '1' else False


def to_int(value: str) -> int:
    return int(value) if value else 0


def to_datetime(value: str) -> Optional[datetime]:
    if not value:
        return None

    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None


def get_formatted_text_props(
        props_name_map: Dict[str, str],
        payload: dict,
        default_value: str = '') -> Dict[str, str]:
    return {props_name_map.get(prop): payload.get(prop, default_value) for prop in props_name_map}


def get_formatted_int_props(
        props_name_map: Dict[str, str],
        payload: dict,
        default_value: int = 0) -> Dict[str, int]:
    return {props_name_map.get(prop): to_int(payload.get(prop, default_value)) for prop in props_name_map}


def get_formatted_bool_props(
        props_name_map: Dict[str, str],
        payload: dict,
        default_value: bool = False) -> Dict[str, bool]:
    return {props_name_map.get(prop): to_bool(payload.get(prop, default_value)) for prop in props_name_map}


def get_formatted_datetime_props(
        props_name_map: Dict[str, str],
        payload: dict,
        default_value: datetime = None) -> Dict[str, datetime]:
    return {props_name_map.get(prop): to_datetime(payload.get(prop, default_value)) for prop in props_name_map}
