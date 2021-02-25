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
    GetCommentsCountOnFormEntriesRequest,
    CommentData
)
from wufoo_rest.api.entry import (
    GetEntriesRequest,
    GetEntriesCountRequest,
    SubmitEntryRequest,
    SubmitEntryResponse,
    EntryData
)
from wufoo_rest.api.report import (
    GetAllReportsRequest,
    GetReportRequest,
    GetReportEntriesRequest,
    GetReportEntriesCountRequest,
    GetReportFieldsRequest,
    ReportData
)


class WufooClient:
    
    def __init__(self, subdomain: str, username: str, password: str):
        base_url = f'https://{subdomain}.wufoo.com/api/v3/'
        self.api_caller = ApiCaller(base_url, username, password)

    def get_all_forms(self) -> List[FormData]:
        req = GetAllFormsRequest()
        return self.api_caller.call(req)
    
    def get_form(self, form_id: str) -> FormData:
        req = GetFormRequest(identifier=form_id)
        return self.api_caller.call(req)
    
    def get_form_fields(self, form_id: str) -> List[FieldData]:
        req = GetFormFieldsRequest(form_identifier=form_id)
        return self.api_caller.call(req)
    
    def get_comments_on_form_entries(self, form_id: str) -> List[CommentData]:
        req = GetCommentsOnFormEntriesRequest(form_identifier=form_id)
        return self.api_caller.call(req)
    
    def get_comments_count(self, form_id: str) -> int:
        req = GetCommentsCountOnFormEntriesRequest(form_identifier=form_id)
        return self.api_caller.call(req)

    def get_entries(self, form_id: str, **kwargs) -> List[EntryData]:
        req = GetEntriesRequest(form_identifier=form_id, **kwargs)
        return self.api_caller.call(req)

    def get_entries_count(self, form_id: str) -> int:
        req = GetEntriesCountRequest(form_identifier=form_id)
        return self.api_caller.call(req)
    
    def submit_entry(self, form_id: str, data: dict) -> SubmitEntryResponse:
        req = SubmitEntryRequest(form_identifier=form_id, fields=data)
        return self.api_caller.call(req)

    def get_all_reports(self) -> List[ReportData]:
        req = GetAllReportsRequest()
        return self.api_caller.call(req)

    def get_report(self, report_id: str) -> ReportData:
        req = GetReportRequest(report_identifier=report_id)
        return self.api_caller.call(req)

    def get_report_entries(self, report_id: str) -> List[EntryData]:
        req = GetReportEntriesRequest(report_identifier=report_id)
        return self.api_caller.call(req)

    def get_report_entries_count(self, report_id: str) -> int:
        req = GetReportEntriesCountRequest(report_identifier=report_id)
        return self.api_caller.call(req)

    def get_report_fields(self, report_id: str) -> List[FieldData]:
        req = GetReportFieldsRequest(report_identifier=report_id)
        return self.api_caller.call(req)
