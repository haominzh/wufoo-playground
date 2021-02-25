import argparse
from wufoo_rest.client import WufooClient
from wufoo_rest.api.entry import (
    Filter,
    Grouping,
    Operator,
    Sorting,
    SortingDirection
)

subdomain = 'fishbowl'
username = 'AOI6-LFKL-VM1Q-IEX9'
password = 'footastic'
TEST_FORM_ID = 's1afea8b1vk0jf7'
TEST_REPORT_ID = 'qa4d98l1ib9or7'

"""
key: command
value: (function, description)
"""
all_showcases = {}
# wf_client = WufooClient(subdomain, username, password)
wf_client = WufooClient.login('XXX', 'fishbowl@wufoo.com', 'XXX', 'fishbowl')


def showcase(*args, **kwargs):
    def register(func):
        command = kwargs['command']
        description = kwargs['description']
        all_showcases[command] = (func, description)
        return func
    return register


@showcase(command='1', description='Show all forms')
def show_all_forms():
    print(wf_client.get_all_forms())


@showcase(command='2', description="Show one form")
def show_one_form():
    print(wf_client.get_form(TEST_FORM_ID))


@showcase(command='3', description="Show all fields of a form")
def show_fields():
    print(wf_client.get_form_fields(TEST_FORM_ID))


@showcase(command='4', description="Show all comments of a form")
def show_all_comments():
    print(wf_client.get_comments_on_form_entries(TEST_FORM_ID))


@showcase(command='5', description="Show comments count")
def show_comments_count():
    print(wf_client.get_comments_count(TEST_FORM_ID))


@showcase(command='6', description="Show entries with filter and sorting")
def show_entries():
    filters = [
        Filter(id='EntryId', operator=Operator.Is_greater_than, value='1'),
        Filter(id='EntryId', operator=Operator.Is_less_than, value='5')
    ]
    print(
        wf_client.get_entries(
            TEST_FORM_ID,
            filters=filters,
            grouping=Grouping.AND,
            sorting=Sorting(id='EntryId', direction=SortingDirection.DESC)
        )
    )


@showcase(command='7', description="Show entries count")
def show_entries_count():
    print(wf_client.get_entries_count(TEST_FORM_ID))


@showcase(command='8', description="Submit entry (succeeded)")
def submit_entry_success():
    values = {
        'Field1': 'Wufoo',
        'Field2': 'Test',
        'Field105': 'API-Test',
        'Field106': '42'
    }
    print(wf_client.submit_entry(TEST_FORM_ID, values))


@showcase(command='9', description="Submit entry (failed)")
def submit_entry_fail():
    values = {
        'Field1': 'Wufoo',
        'Field2': 'Test',
        'Field106': 'Fail'
    }
    print(wf_client.submit_entry(TEST_FORM_ID, values))


@showcase(command='10', description="Show all reports")
def show_all_reports():
    print(wf_client.get_all_reports())
    

@showcase(command='11', description="Show one report")
def show_report():
    print(wf_client.get_report(TEST_REPORT_ID))


@showcase(command='12', description="Show report entries")
def show_report_entries():
    print(wf_client.get_report_entries(TEST_REPORT_ID))


@showcase(command='13', description="Show report entries count")
def show_report_entries():
    print(wf_client.get_report_entries_count(TEST_REPORT_ID))


@showcase(command='14', description="Show report fields")
def show_report_entries():
    print(wf_client.get_report_fields(TEST_REPORT_ID))


@showcase(command='15', description="Show report widgets")
def show_report_widgets():
    print(wf_client.get_report_widgets(TEST_REPORT_ID))


@showcase(command='16', description="Show all users")
def show_all_users():
    print(wf_client.get_all_users())


@showcase(command='17', description="Put and delete webhook")
def put_webhook():
    wh_response = wf_client.put_webhook(TEST_FORM_ID, 'https://www.wufoo.com', 'secret123', True)
    print(f'Webhook {wh_response.hash} is created on form {TEST_FORM_ID}')
    wh_response = wf_client.delete_webhook(TEST_FORM_ID, wh_response.hash)
    print(f'Webhook {wh_response.hash} on form {TEST_FORM_ID} is deleted')


def main():
    parser = argparse.ArgumentParser(description="Wufoo rest API showcases")
    parser.add_argument('-l', '--list', action='store_true', help='List all commands')
    parser.add_argument('-c', '--command', type=str, help='Showcase command')
    args = parser.parse_args()

    if args.list:
        for key in all_showcases:
            print(f'Command {key} | Description: {all_showcases.get(key)[1]}')
    elif args.command:
        if args.command not in all_showcases:
            raise Exception(f'Command {args.command} not supported')
        all_showcases.get(args.command)[0]()


if __name__ == '__main__':
    main()
