# -*- coding: utf-8 -*-
import json
from unittest import TestCase
from hl7tojson import parser


class TestParser(TestCase):
    def setUp(self):
        self.message = """
            MSH|^~\&|MegaReg|XYZHospC|SuperOE|XYZImgCtr|20060529090131-0500||ADT^A01^ADT_A01|01052901|P|2.5\rEVN||200605290901||||200605290900\rPID|||56782445^^^UAReg^PI||KLEINSAMPLE^BARRY^Q^JR||19620910|M||2028-9^^HL70005^RA99113^^XYZ|260 GOODWIN CREST DRIVE^^BIRMINGHAM^AL^35209^^M~NICKELL’S PICKLES^10000 W 100TH AVE^BIRMINGHAM^AL^35200^^O|||||||0105I30001^^^99DEF^AN\rPV1||I|W^389^1^UABH^^^^3||||12345^MORGAN^REX^J^^^MD^0010^UAMC^L||67890^GRAINGER^LUCY^X^^^MD^0010^UAMC^L|MED|||||A0||13579^POTTER^SHERMAN^T^^^MD^0010^UAMC^L|||||||||||||||||||||||||||200605290900\rOBX|1|NM|^Body Height||1.80|m^Meter^ISO+|||||F\rOBX|2|NM|^Body Weight||79|kg^Kilogram^ISO+|||||F\rAL1|1||^ASPIRIN\rDG1|1||786.50^CHEST PAIN, UNSPECIFIED^I9|||A\r
        """

    def test_parse_hl7_message(self):
        h = parser.parse_hl7_message(self.message)
        assert h is not None
        assert len(h) == 8

    def test_update_description(self):
        h = parser.parse_hl7_message(self.message)
        new_message = parser.update_description(0, h)
        assert hasattr(new_message, 'desc')

    def test_validate_message(self):
        h = parser.parse_hl7_message(self.message)
        assert parser.validate_segments(h)

    def test_hl7_message_to_dict(self):
        h = parser.parse_hl7_message(self.message)
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

