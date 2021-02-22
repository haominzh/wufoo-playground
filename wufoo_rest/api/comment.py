import requests
from typing import NamedTuple, List
from datetime import datetime

from wufoo_rest.api_caller import execute
from wufoo_rest.utils import to_datetime

TEXT_PROPS = {
    'CommentId': 'comment_id',
    'EntryId': 'entry_id',
    'Text': 'text',
    'CommentedBy': 'commented_by'
}

DATETIME_PROPS = {
    'DateCreated': 'date_created'
}


class GetCommentsOnFormEntriesRequest(NamedTuple):
    form_identifier: str
    entry_id: str = None
    page_start: int = 0
    page_size: int = 25


class CommentData(NamedTuple):
    comment_id: str
    entry_id: str
    text: str
    commented_by: str
    date_created: datetime

    @classmethod
    def from_payload(cls, payload):
        text_props = {TEXT_PROPS.get(prop): payload.get(prop, '') for prop in TEXT_PROPS}
        datetime_props = {DATETIME_PROPS.get(prop): to_datetime(payload.get(prop, None)) for prop in DATETIME_PROPS}

        return cls(**text_props, **datetime_props)


@execute.register(GetCommentsOnFormEntriesRequest)
def _(request: GetCommentsOnFormEntriesRequest, base_url: str, username: str, password: str) -> List[CommentData]:
    url = base_url + f'forms/{request.form_identifier}/comments.json'
    params = {}

    if request.entry_id:
        params['entryId'] = request.entry_id

    if request.page_start > 0:
        params['pageStart'] = request.page_start
    
    if request.page_size != 25 and request.page_size > 0:
        params['pageSize'] = min(request.page_size, 100)

    response = requests.get(url, params=params, auth=(username, password))
    response.raise_for_status()
    data = response.json()
    return [CommentData.from_payload(f) for f in data['Comments']]


class GetCommentsCountOnFormEntries(NamedTuple):
    form_identifier: str


@execute.register(GetCommentsCountOnFormEntries)
def _(request: GetCommentsCountOnFormEntries, base_url: str, username: str, password: str) -> int:
    url = base_url + f'forms/{request.form_identifier}/comments/count.json'

    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    data = response.json()
    return data['Count']