from typing import List

from wufoo_rest.api_caller import ApiCaller
from wufoo_rest.api.form import (
    GetAllFormsRequest,
    GetFormRequest,
    FormData
)
from wufoo_rest.api.field import (
    GetFormFieldsRequest,
    FieldData
)
from wufoo_rest.api.comment import (
    GetCommentsOnFormEntriesRequest,
    GetCommentsCountOnFormEntries,
    CommentData
)
from wufoo_rest.api.entry import (
    GetEntriesRequest,
    GetEntriesCountRequest,
    SubmitEntryRequest,
    SubmitEntryResponse,
    EntryData
)

base_url = 'https://fishbowl.wufoo.com/api/v3/'
username = 'AOI6-LFKL-VM1Q-IEX9'
password = 'footastic'

api_caller = ApiCaller(base_url, username, password)


def get_all_forms() -> List[FormData]:
    req = GetAllFormsRequest()
    return api_caller.call(req)


def get_form(form_id: str) -> FormData:
    req = GetFormRequest(identifier=form_id)
    return api_caller.call(req)


def get_form_fields(form_id: str) -> List[FieldData]:
    req = GetFormFieldsRequest(form_identifier=form_id)
    return api_caller.call(req)


def get_comments_on_form_entries(form_id: str) -> List[CommentData]:
    req = GetCommentsOnFormEntriesRequest(form_identifier=form_id)
    return api_caller.call(req)


def get_comments_count(form_id: str) -> int:
    req = GetCommentsCountOnFormEntries(form_identifier=form_id)
    return api_caller.call(req)


def get_entries(form_id: str, **kwargs) -> List[EntryData]:
    req = GetEntriesRequest(form_identifier=form_id, **kwargs)
    return api_caller.call(req)


def get_entries_count(form_id: str) -> int:
    req = GetEntriesCountRequest(form_identifier=form_id)
    return api_caller.call(req)


def submit_entry(form_id: str, data: dict) -> SubmitEntryResponse:
    req = SubmitEntryRequest(form_identifier=form_id, fields=data)
    return api_caller.call(req)
