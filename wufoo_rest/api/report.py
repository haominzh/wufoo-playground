import requests
from typing import NamedTuple, List
from datetime import datetime

from wufoo_rest.api_caller import execute
from wufoo_rest.utils import (
    get_formatted_bool_props,
    get_formatted_text_props,
    get_formatted_datetime_props
)
from wufoo_rest.api.entry import EntryData
from wufoo_rest.api.field import FieldData

TEXT_PROPS = {
    'Name': 'name',
    'Url': 'url',
    'Description': 'description',
    'Hash': 'hash',
    'LinkFields': 'link_fields',
    'LinkEntries': 'link_entries',
    'LinkEntriesCount': 'link_entries_count',
    'LinkWidgets': 'link_widgets'
}

BOOL_PROPS = {
    'IsPublic': 'is_public'
}

DATETIME_PROPS = {
    'DateCreated': 'date_created',
    'DateUpdated': 'date_updated'
}


class GetAllReportsRequest(NamedTuple):
    pass


class ReportData(NamedTuple):
    name: str
    description: str
    url: str
    is_public: bool
    date_created: datetime
    date_updated: datetime
    hash: str
    link_fields: str
    link_entries: str
    link_entries_count: str
    link_widgets: str

    @classmethod
    def from_payload(cls, payload):
        text_prop = get_formatted_text_props(TEXT_PROPS, payload)
        bool_props = get_formatted_bool_props(BOOL_PROPS, payload)
        datetime_props = get_formatted_datetime_props(DATETIME_PROPS, payload)

        return cls(**text_prop, **bool_props, **datetime_props)


@execute.register(GetAllReportsRequest)
def _(request: GetAllReportsRequest, base_url: str, username: str, password: str) -> List[ReportData]:
    url = base_url + 'reports.json'

    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    data = response.json()
    return [ReportData.from_payload(f) for f in data['Reports']]


class GetReportRequest(NamedTuple):
    report_identifier: str


@execute.register(GetReportRequest)
def _(request: GetReportRequest, base_url: str, username: str, password: str) -> ReportData:
    url = base_url + f'reports/{request.report_identifier}.json'
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    data = response.json()['Reports']
    return ReportData.from_payload(data[0])


class GetReportEntriesRequest(NamedTuple):
    report_identifier: str


@execute.register(GetReportEntriesRequest)
def _(request: GetReportEntriesRequest, base_url: str, username: str, password: str) -> List[EntryData]:
    url = base_url + f'reports/{request.report_identifier}/entries.json'
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    data = response.json()['Entries']
    return [EntryData.from_payload(entry) for entry in data]


class GetReportEntriesCountRequest(NamedTuple):
    report_identifier: str


@execute.register(GetReportEntriesCountRequest)
def _(request: GetReportEntriesCountRequest, base_url: str, username: str, password: str) -> int:
    url = base_url + f'reports/{request.report_identifier}/entries/count.json'
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    return response.json()['EntryCount']


class GetReportFieldsRequest(NamedTuple):
    report_identifier: str


@execute.register(GetReportFieldsRequest)
def _(request: GetReportFieldsRequest, base_url: str, username: str, password: str) -> List[FieldData]:
    url = base_url + f'reports/{request.report_identifier}/fields.json'
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    data = response.json()['Fields']
    return [FieldData.from_payload(f) for f in data]
