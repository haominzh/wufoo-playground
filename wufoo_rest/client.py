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
    GetWidgetsRequest,
    ReportData,
    WidgetsData
)
from wufoo_rest.api.user import (
    GetAllUsersRequest,
    UserData
)
from wufoo_rest.api.webhook import (
    PutWebhookRequest,
    DeleteWebhookRequest,
    PutWebhookResponse,
    DeleteWebhookResponse,
)
from wufoo_rest.api.login import RetrieveApiKeyRequest, retrieve_api_key


class WufooClient:
    
    def __init__(self, subdomain: str, username: str, password: str):
        base_url = f'https://{subdomain}.wufoo.com/api/v3/'
        self.api_caller = ApiCaller(base_url, username, password)

    @classmethod
    def login(cls, integration_key: str, email: str, password: str, subdomain: str):
        """
        This request allows approved partners to access users API Keys.
        This is useful for custom integrations that need to make API requests on behalf of Wufoo users.
        For example, Zapier uses this method to set up new integrations, without requiring users to
        use or even know their own API Key.
        """
        req = RetrieveApiKeyRequest(integration_key, email, password, subdomain)
        key_response = retrieve_api_key(req)
        return cls(key_response.subdomain, username=key_response.api_key, password=key_response.api_key)

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

    def get_report_widgets(self, report_id: str) -> List[WidgetsData]:
        req = GetWidgetsRequest(report_identifier=report_id)
        return self.api_caller.call(req)

    def get_all_users(self) -> List[UserData]:
        req = GetAllUsersRequest()
        return self.api_caller.call(req)

    def put_webhook(self, form_id: str, url: str, handshake_key: str, metadata: bool = False) -> PutWebhookResponse:
        req = PutWebhookRequest(form_id, url, handshake_key, metadata)
        return self.api_caller.call(req)

    def delete_webhook(self, form_id: str, webhook_hash: str) -> DeleteWebhookResponse:
        req = DeleteWebhookRequest(form_id, webhook_hash)
        return self.api_caller.call(req)
