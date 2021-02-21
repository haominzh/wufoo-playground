from functools import singledispatch


class ApiCaller:

    def __init__(self, base_url: str, username: str, password: str):
        self._base_url = base_url
        self._username = username
        self._password = password

    @property
    def base_url(self):
        return self._base_url

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    def call(self, request):
        return execute(request, self.base_url, self.username, self.password)

@singledispatch
def execute(request, base_url: str, username: str, password: str):
    raise NotImplementedError('Unsupported type')

