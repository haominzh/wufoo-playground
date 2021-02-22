import requests
from typing import NamedTuple, List
from dataclasses import dataclass

from wufoo_rest.api_caller import execute
from wufoo_rest.utils import to_bool, to_int

FIELD_TEXT_PROPERTY = {
    'Title': 'title',
    'Instructions': 'instructions',
    'ClassNames': 'class_names',
    'ID': 'id',
    'Label': 'label',
    'DefaultVal': 'default_val'
}

FIELD_BOOL_PROPERTY = {
    'IsRequired': 'is_required'
}

FIELD_INT_PROPERTY = {
    'Page': 'page'
}

CHOICES_FILED_PROPERTY = {
    'HasOtherField': 'has_other_field',
    'Score': 'score'
}

FIELD_DATA_PROPERTY = {
    'Type': 'field_type',
    'IsSystem': 'is_system'
}


class GetFormFieldsRequest(NamedTuple):
    form_identifier: str
    system: bool = False


def get_field_props(payload):
    text_props = {FIELD_TEXT_PROPERTY.get(prop): payload.get(prop, '') for prop in FIELD_TEXT_PROPERTY}
    int_props = {FIELD_INT_PROPERTY.get(prop): to_int(payload.get(prop, 0)) for prop in FIELD_INT_PROPERTY}
    bool_props = {FIELD_BOOL_PROPERTY.get(prop): to_bool(payload.get(prop, False)) for prop in FIELD_BOOL_PROPERTY}
    return {**text_props, **int_props, **bool_props}


@dataclass
class Field:
    title: str
    instructions: str
    is_required: bool
    class_names: str
    id: str
    label: str
    default_val: str
    page: int

    @classmethod
    def from_payload(cls, payload):
        props = get_field_props(payload)
        return cls(**props)


@dataclass
class ChoicesField(Field):
    has_other_field: bool
    score: int

    @classmethod
    def from_payload(cls, payload):
        field_props = get_field_props(payload)
        choices_props = {CHOICES_FILED_PROPERTY.get(prop): payload.get(prop, None) for prop in CHOICES_FILED_PROPERTY}
        return cls(**field_props, **choices_props)


@dataclass
class FieldData(Field):
    field_type: str
    is_system: bool
    sub_fields: List[Field] = None
    choices: List[ChoicesField] = None

    @classmethod
    def from_payload(cls, payload):
        field_props = get_field_props(payload)
        field_data_props = {FIELD_DATA_PROPERTY.get(prop): payload.get(prop, None) for prop in FIELD_DATA_PROPERTY}
        sub_fields_props = {}
        sf_data = payload.get('SubFields', None)
        if sf_data:
            sub_fields_props = {'sub_fields': [Field.from_payload(f) for f in sf_data]}
        
        choices_field_props = {}
        choices_field_data = payload.get('Choices', None)
        if choices_field_data:
            choices_field_props = {'choices': [ChoicesField.from_payload(f) for f in choices_field_data]}

        return cls(**field_props, **field_data_props, **sub_fields_props, **choices_field_props)


@execute.register(GetFormFieldsRequest)
def _(request: GetFormFieldsRequest, base_url: str, username: str, password: str) -> List[FieldData]:
    url = base_url + f'forms/{request.form_identifier}/fields.json'
    params = {}

    """
    https://wufoo.github.io/docs/?python#form-fields

    If you set system to any value (system=true, system=false, etc), the fields will be included, 
    so if you don’t want the System Fields, leave the system parameter out (Don’t just set it to false).
    """
    if request.system:
        params['system'] = 'true'

    response = requests.get(url, params=params, auth=(username, password))
    response.raise_for_status()
    data = response.json()
    return [FieldData.from_payload(f) for f in data['Fields']]
