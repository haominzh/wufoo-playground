import requests
from typing import NamedTuple


class RetrieveApiKeyRequest(NamedTuple):
    integration_key: str
    email: str
    password: str
    subdomain: str


class ApiKeyResponse(NamedTuple):
    api_key: str
    user_link: str
    subdomain: str


def retrieve_api_key(request: RetrieveApiKeyRequest) -> ApiKeyResponse:
    url = 'https://wufoo.com/api/v3/login.json'
    data = {
        'integrationKey': request.integration_key,
        'email': request.email,
        'password': request.password,
        'subdomain': request.subdomain
    }
    response = requests.post(url, data)
    response.raise_for_status()
    payload = response.json()
    return ApiKeyResponse(payload['ApiKey'], payload['UserLink'], payload['Subdomain'])
