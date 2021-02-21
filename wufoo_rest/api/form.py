import requests
from typing import NamedTuple, List
from datetime import datetime

from wufoo_rest.api_caller import execute
from utils import to_bool, to_datetime, to_int

TEXT_PROPERTIES = {
    'Name': 'name',
    'Description': 'description',
    'RedirectMessage': 'redirect_message',
    'Url': 'url',
    'Email': 'email',
    'Language': 'language',
    'Hash': 'hash',
    'LinkFields': 'link_fields',
    'LinkEntries': 'link_entries',
    'LinkEntriesCount': 'link_entries_count'
}

INT_PROPERTIES = {
    'EntryLimit': 'entry_limit'
}

BOOL_PROPERTIES = {
    'IsPublic': 'is_public'
}

DATETIME_PROPERTIES = {
    'StartDate': 'start_date',
    'EndDate': 'end_date',
    'DateCreated': 'date_created',
    'DateUpdated': 'date_updated'
}


class GetAllFormsRequest(NamedTuple):
    include_today_count: bool = False


class FormData(NamedTuple):
    name: str
    description: str
    redirect_message: str
    url: str
    email: str
    language: str
    hash: str
    link_fields: str
    link_entries: str
    link_entries_count: str
    entry_limit: int
    is_public: bool
    start_date: datetime
    end_date: datetime
    date_created: datetime
    date_updated: datetime

    @classmethod
    def from_payload(cls, payload):
        text_props = {TEXT_PROPERTIES.get(prop): payload.get(prop, '') for prop in TEXT_PROPERTIES}
        int_props = {INT_PROPERTIES.get(prop): to_int(payload.get(prop, 0)) for prop in INT_PROPERTIES}
        bool_props = {BOOL_PROPERTIES.get(prop): to_bool(payload.get(prop, False)) for prop in BOOL_PROPERTIES}
        datetime_props = {DATETIME_PROPERTIES.get(prop): to_datetime(payload.get(prop, None)) for prop in DATETIME_PROPERTIES}

        return cls(**text_props, **int_props, **bool_props, **datetime_props)


@execute.register(GetAllFormsRequest)
def _(request: GetAllFormsRequest, base_url: str, username: str, password: str) -> List[FormData]:
    url = base_url + 'forms.json'
    params = {}

    # Notice: Do not include includeTodayCount in params if it's False.
    # It returns EntryCountToday if includeTodayCount presents, even if the value is False
    if request.include_today_count:
        params['includeTodayCount'] = 'true'

    response = requests.get(url, params=params, auth=(username, password))
    response.raise_for_status()
    data = response.json()
    return [FormData.from_payload(f) for f in data['Forms']]


class GetFormRequest(NamedTuple):
    identifier: str
    include_today_count: bool = False

@execute.register(GetFormRequest)
def _(request: GetFormRequest, base_url: str, username: str, password: str) -> FormData:
    url = base_url + f'forms/{request.identifier}.json'
    params = {}
    # Notice: Do not include includeTodayCount in params if it's False.
    # It returns EntryCountToday if includeTodayCount presents, even if the value is False
    if request.include_today_count:
        params['includeTodayCount'] = 'true'

    response = requests.get(url, params=params, auth=(username, password))
    response.raise_for_status()
    data = response.json()
    return FormData.from_payload(data['Forms'][0])