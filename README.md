### Wufoo v3 REST API playground
A simple playground of Wufoo v3 APIs. https://wufoo.github.io/docs/#

#### Supported functionalities:
* Fetch forms
* Fetch single form
* Fetch form fields
* Fetch form comments
* Fetch form comments count
* Fetch entries (with filter and sorting)
* Fetch entries count
* Submit entry
* Fetch reports
* Fetch single report
* Fetch report entries
* Fetch report entries count
* Fetch report fields
* Fetch report widgets
* Fetch all users
* Add/Delete webhook
* Retrieve API key

#### Project structure:
```
wufoo-playground
    │──── playground.py                   # main method for show cases
    │──── README.md
    │──── requirements.txt
    │──── setup.py
    └──── /wufoo_rest
              │──── __init__.py
              │──── client.py             # Wufoo rest client
              │──── api_caller.py         # An api delegater
              │──── utils.py              # util functions
              └──── /api
                     │──── __init__.py
                     │──── comment.py     # Comments requests and responses
                     │──── entry.py       # Entry requests and responses
                     │──── field.py       # Field requests and responses
                     │──── report.py      # Report requests and responses
                     │──── form.py        # Form requests and responses
                     │──── user.py        # User requests and responses
                     │──── webhook.py     # Webhook requests and responses
                     └──── login.py       # Retrieve API key
```

#### Install:
```
pip install git+https://github.com/haominzh/wufoo-playground
```

#### Example:
```python
import csv
import io
from wufoo_rest.client import WufooClient

subdomain = 'fishbowl'
username = 'AOI6-LFKL-VM1Q-IEX9'
password = 'footastic'

ENTRY = """FormID,Field1,Field2,Field105,Field106
s1afea8b1vk0jf7,Wufoo,test,API-Test,42
s1afea8b1vk0jf7,Wufoo,Test,,Failed
"""

wf_client = WufooClient(subdomain, username, password)

reader = csv.DictReader(io.StringIO(ENTRY))
for row in reader:
    form_id = row.pop('FormID')
    res = wf_client.submit_entry(form_id, row)
    if res.success:
        print(f'Submit {row} to form [{form_id}] succeeded')
    else:
        print(f'Submit {row} to form [{form_id}] Failed')
        print('=' * 50)
        print(
            f"{res.detail['ErrorText']}\n{res.detail['FieldErrors']}"
        )
        print('=' * 50)
```
Output:
```
Submit {'Field1': 'Wufoo', 'Field2': 'test', 'Field105': 'API-Test', 'Field106': '42'} to form [s1afea8b1vk0jf7] succeeded
Submit {'Field1': 'Wufoo', 'Field2': 'Test', 'Field105': '', 'Field106': 'Failed'} to form [s1afea8b1vk0jf7] Failed
==================================================
Errors have been <b>highlighted</b> below.
[{'ID': 'Field105', 'ErrorText': 'This field is required. Please enter a value.'}, {'ID': 'Field106', 'ErrorText': 'Please enter a numeric value.'}]
==================================================
```
