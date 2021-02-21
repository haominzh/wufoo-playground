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
    Filter,
    Grouping,
    Operator,
    Sorting,
    SortingDirection,
    EntryData
)

base_url = 'https://fishbowl.wufoo.com/api/v3/'
username = 'AOI6-LFKL-VM1Q-IEX9'
password = 'footastic'

TEST_FORM_ID = 's1afea8b1vk0jf7'

api_caller = ApiCaller(base_url, username, password)

def main():
    """show all forms"""
    # print(get_all_forms())

    """show one form"""
    # print(get_form(TEST_FORM_ID))

    """show all fields of a form"""
    # print(get_form_fields(TEST_FORM_ID))

    """show all comments of a form entries"""
    # print(get_comments_on_form_entries(TEST_FORM_ID))

    """show comments count of a form"""
    # print(get_comments_count(TEST_FORM_ID))

    """show entries with filters"""
    # filters = [
    #     Filter(id='EntryId', operator=Operator.Is_greater_than, value='1'),
    #     Filter(id='EntryId', operator=Operator.Is_less_than, value='5')
    # ]
    # print(
    #     get_entries(
    #         TEST_FORM_ID, 
    #         filters=filters, 
    #         grouping=Grouping.AND, 
    #         sorting=Sorting(id='EntryId', direction=SortingDirection.DESC)
    #     )
    # )

    """show entries count"""
    # print(get_entries_count(TEST_FORM_ID))

    """submit entry (success)"""
    # values = {
    #     'Field1' : 'Wufoo',
    #     'Field2' : 'Test',
    #     'Field105' : 'API-Test',
    #     'Field106' : '42'
    # }
    # print(submit_entry(TEST_FORM_ID, values))

    # """submit entry (fail)"""
    # values = {
    #     'Field1' : 'Wufoo',
    #     'Field2' : 'Test',
    #     'Field106' : 'Fail'
    # }
    # print(submit_entry(TEST_FORM_ID, values))


    
def get_all_forms() -> List[FormData]:
    req = GetAllFormsRequest()
    return api_caller.call(req)

def get_form(id: str) -> FormData:
    req = GetFormRequest(identifier=id)
    return api_caller.call(req)

def get_form_fields(id: str) -> List[FieldData]:
    req = GetFormFieldsRequest(form_identifier=id)
    return api_caller.call(req)

def get_comments_on_form_entries(id: str) -> List[CommentData]:
    req = GetCommentsOnFormEntriesRequest(form_identifier=id)
    return api_caller.call(req)

def get_comments_count(id: str) -> int:
    req = GetCommentsCountOnFormEntries(form_identifier=id)
    return api_caller.call(req)

def get_entries(id: str, **kwargs) -> List[EntryData]:
    req = GetEntriesRequest(form_identifier=id, **kwargs)
    return api_caller.call(req)

def get_entries_count(id: str) -> int:
    req = GetEntriesCountRequest(form_identifier=id)
    return api_caller.call(req)

def submit_entry(id: str, data: dict) -> SubmitEntryResponse:
    req = SubmitEntryRequest(form_identifier=id, fields=data)
    return api_caller.call(req)

if __name__ == '__main__':
    main()