# -*- coding: utf-8 -*-
from unittest import TestCase

from hl7tojson import parser
from hl7tojson import validator
from tests import samples


class TestValidator(TestCase):
    def setUp(self):
        self.valid_message = parser.parse_hl7_message(samples.message1)

    def test_import_all(self):
        from hl7tojson.validator import *
        assert 'validate' in locals()
        assert 'validate_message' not in locals()

    # def test_validate_valid_message(self):
    #     assert validator.validate_message(self.valid_message)

    def test_validate_message_containing_not_valid_segments(self):
        hl7_message = parser.parse(samples.message4)
        res = validator.validate_message(hl7_message)
        assert not bool(res['status'])
