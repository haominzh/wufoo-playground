import requests
from typing import NamedTuple

from wufoo_rest.api_caller import execute


class PutWebhookRequest(NamedTuple):
    form_identifier: str
    url: str
    handshake_key: str
    metadata: bool = False


class PutWebhookResponse(NamedTuple):
    hash: str


@execute.register(PutWebhookRequest)
def _(request: PutWebhookRequest, base_url: str, username: str, password: str) -> PutWebhookResponse:
    url = base_url + f'forms/{request.form_identifier}/webhooks.json'
    data = {
        'url': request.url,
        'handshakeKey': request.handshake_key,
        'metadata': request.metadata
    }
    response = requests.put(url, data, auth=(username, password))
    response.raise_for_status()
    data = response.json()['WebHookPutResult']
    return PutWebhookResponse(data['Hash'])


class DeleteWebhookRequest(NamedTuple):
    form_identifier: str
    webhook_hash: str


class DeleteWebhookResponse(NamedTuple):
    hash: str


@execute.register(DeleteWebhookRequest)
def _(request: DeleteWebhookRequest, base_url: str, username: str, password: str) -> DeleteWebhookResponse:
    url = base_url + f'forms/{request.form_identifier}/webhooks/{request.webhook_hash}.json'
    response = requests.delete(url, auth=(username, password))
    response.raise_for_status()
    data = response.json()['WebHookDeleteResult']
    return DeleteWebhookResponse(data['Hash'])
