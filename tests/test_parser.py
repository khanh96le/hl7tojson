# -*- coding: utf-8 -*-
import json
from unittest import TestCase
from hl7tojson import parser
from tests.samples import message1, message2


class TestParserValidate(TestCase):
    def setUp(self):
        pass

    def test_parse_hl7_message(self):
        h = parser.parse_hl7_message(message1)
        assert h is not None
        assert len(h) == 8

    def test_update_description(self):
        h = parser.parse_hl7_message(message1)
        new_message = parser.update_description(0, h)
        assert hasattr(new_message, 'desc')

    def test_validate_message(self):
        h = parser.parse_hl7_message(message1)
        assert parser.validate_segments(h)

    def test_hl7_message_to_dict(self):
        h = parser.parse_hl7_message(message1)
        new_message = parser.update_description(0, h)
        data = parser.hl7_message_to_dict(new_message)
        assert data is not None
        print(json.dumps(data, indent=4))
        assert data['info']['message_type'] == 'ADT_A01'
        assert data['info']['message_description'] == 'Admit/Visit Notification'

        assert data['segments'][0]['type'] == 'MSH'
        assert data['segments'][0]['description'] == 'Message Header'

        msh_fields = data['segments'][0]['fields']
        assert msh_fields[0]['id'] == 1
        assert msh_fields[0]['description'] == 'Field Separator'
        assert msh_fields[0]['data'] == '|'

        message_type_repetitions = msh_fields[7]['repetitions']
        assert message_type_repetitions[0]['data'] == 'ADT^A01^ADT_A01'
        assert message_type_repetitions[0]['description'] == 'Message Type'

        h = parser.parse_hl7_message(message2)
        new_message = parser.update_description(0, h)
        data = parser.hl7_message_to_dict(new_message)
        assert data is not None

    def test_parser(self):
        data = parser.parse(message1)
        assert data is not None
