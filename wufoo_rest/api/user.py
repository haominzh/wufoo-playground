import requests
from typing import NamedTuple, List

from wufoo_rest.api_caller import execute
from wufoo_rest.utils import (
    get_formatted_bool_props,
    get_formatted_text_props
)


TEXT_PROPS = {
    'User': 'user',
    'Email': 'email',
    'Timezone': 'timezone',
    'Company': 'company',
    'ApiKey': 'api_key',
    'Hash': 'hash',
    'ImageUrl': 'image_url'
}

BOOL_PROPS = {
    'IsAccountOwner': 'is_account_owner',
    'CreateForms': 'create_forms',
    'CreateReports': 'create_reports',
    'CreateThemes': 'create_themes',
    'AdminAccess': 'admin_access',
    'HttpsEnabled': 'https_enabled'
}


class GetAllUsersRequest(NamedTuple):
    pass


class UserData(NamedTuple):
    user: str
    email: str
    timezone: str
    company: str
    is_account_owner: bool
    create_forms: bool
    create_reports: bool
    create_themes: bool
    admin_access: bool
    api_key: str
    hash: str
    image_url: str
    https_enabled: bool

    @classmethod
    def from_payload(cls, payload):
        text_props = get_formatted_text_props(TEXT_PROPS, payload)
        bool_props = get_formatted_bool_props(BOOL_PROPS, payload)

        return cls(**text_props, **bool_props)


@execute.register(GetAllUsersRequest)
def _(request: GetAllUsersRequest, base_url: str, username: str, password: str) -> List[UserData]:
    url = base_url + 'users.json'
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    data = response.json()['Users']
    return [UserData.from_payload(user) for user in data]
