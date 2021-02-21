import requests
import re
import urllib.parse
from typing import NamedTuple, List, Dict
from datetime import datetime
from enum import Enum

from wufoo_rest.api_caller import execute
from utils import to_datetime

TEXT_PROPS = {
    'EntryId': 'entry_id',
    'CreatedBy': 'created_by',
    'UpdatedBy': 'updated_by'
}

DATETIME_PROPS = {
    'DateCreated': 'date_created',
    'DateUpdated': 'date_updated'
}

SYSTEM_PROPS = [
    'IP', 
    'CompleteSubmission', 
    'Status',
    'PurchaseTotal', 
    'Currency', 
    'TransactionId', 
    'MerchantType',
    'Immutable'
]

field_pattern = re.compile('^Field\d+')


class Grouping(Enum):
    AND = 1
    OR = 2


class SortingDirection(Enum):
    ASC = 1
    DESC = 2


class Operator(Enum):
    Contains = 1
    Does_not_contain = 2
    Begins_with = 3
    Ends_with = 4
    Is_less_than = 5
    Is_greater_than = 6
    Is_on = 7
    Is_before = 8
    Is_after = 9
    Is_not_equal_to = 10
    Is_equal_to = 11
    Is_not_NULL = 12


class Filter(NamedTuple):
    id: str
    operator: Operator
    value: str


class Sorting(NamedTuple):
    id: str
    direction: SortingDirection

def convert_filter_to_param(filter: Filter) -> str:
    return f'{filter.id}+{filter.operator.name}+{filter.value}'


class GetEntriesRequest(NamedTuple):
    form_identifier: str
    system: bool = False
    page_start: int = 0
    page_size: int = 25
    filters: List[Filter] = None
    grouping: Grouping = None
    sorting: Sorting = None

class EntryData(NamedTuple):
    entry_id: str
    date_created: datetime
    created_by: str
    date_updated: datetime
    updated_by: str
    fields: Dict[str, str]
    system: Dict[str, str]

    @classmethod
    def from_payload(cls, payload, system: bool = False):
        text_props = {TEXT_PROPS.get(prop): payload.get(prop, '') for prop in TEXT_PROPS}
        datetime_props = {DATETIME_PROPS.get(prop): to_datetime(payload.get(prop, None)) for prop in DATETIME_PROPS}
        field_props = {k: payload.get(k) for k in payload if field_pattern.match(k)}
        system_props = {}
        if system:
            system_props = {k: payload.get(k) for k in SYSTEM_PROPS if k in payload}
        return cls(fields=field_props, system=system_props, **text_props, **datetime_props)

@execute.register(GetEntriesRequest)
def _(request: GetEntriesRequest, base_url: str, username: str, password: str) -> List[EntryData]:
    url = base_url + f'forms/{request.form_identifier}/entries.json'
    params = {}

    """
    https://wufoo.github.io/docs/?python#form-fields

    If you set system to any value (system=true, system=false, etc), the fields will be included, 
    so if you don’t want the System Fields, leave the system parameter out (Don’t just set it to false).
    """
    if request.system:
        params['system'] = 'true'

    if request.page_start > 0:
        params['pageStart'] = request.page_start
    
    if request.page_size != 25 and request.page_size > 0:
        params['pageSize'] = min(request.page_size, 100)

    if request.filters:
        if len(request.filters) > 1 and not request.grouping:
            raise Exception('Grouping is missing')
        idx = 1
        for f in request.filters:
            params[f'Filter{idx}'] = convert_filter_to_param(f)
            idx += 1
        
        if len(request.filters) > 1:
            params['match'] = request.grouping.name

    if request.sorting:
        params['sort'] = request.sorting.id
        params['sortDirection'] = request.sorting.direction.name

    # Server returns 500 if encode '+' as %2B
    params_str = urllib.parse.urlencode(params, safe=':+')

    response = requests.get(url, params=params_str, auth=(username, password))
    response.raise_for_status()
    data = response.json()['Entries']
    return [EntryData.from_payload(e, system=request.system) for e in data]

    
class GetEntriesCountRequest(NamedTuple):
    form_identifier: str

@execute.register(GetEntriesCountRequest)
def _(request: GetEntriesCountRequest, base_url: str, username: str, password: str) -> int:
    url = base_url + f'forms/{request.form_identifier}/entries/count.json'

    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    data = response.json()
    return data['EntryCount']


class SubmitEntryRequest(NamedTuple):
    form_identifier: str
    fields: Dict[str, str]


class SubmitEntryResponse(NamedTuple):
    response: dict

@execute.register(SubmitEntryRequest)
def _(request: SubmitEntryRequest, base_url: str, username: str, password: str) -> SubmitEntryResponse:
    url = base_url + f'forms/{request.form_identifier}/entries.json'
    response = requests.post(url, data=request.fields, auth=(username, password))
    response.raise_for_status()
    return SubmitEntryResponse(response.json())