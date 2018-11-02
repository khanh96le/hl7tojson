# -*- coding: utf-8 -*-
"""
This module expose a function call :py:func:`validator` to validate data of a
HL7 message
"""
from collections import Counter

import hl7

from hl7tojson import parser
from hl7tojson.dictionary import Dictionary

__all__ = ['validate']

dictionary = Dictionary.Instance()

INF = 100000000
cardinality_rules = {
    (0, 0): (0, INF),
    (0, 1): (0, 1),
    (1, 0): (1, INF),
    (1, 1): (1, 1),
}


def validate(message):
    """Validate a HL7 message from messages, segments to fields

    :param message: instance of :py:class:`hl7.Message`
    :rtype: bool
    """
    if not validate_message(message):
        return False
    return True


def validate_message(message):
    """Validate structure segments of a message. The following factors are
    being validated:
        - name of segments
        - number of appearances of each segment

    :param: message - instance of :py:class:`hl7.Message`
    :rtype: dict

        {
            'status': 1
        }

        {
            'status': 0,
            'error_type': 'message',
            'error_data': [
                {
                    'position': <int>
                    'description': <string>
                }
            ]
        }
    """
    messages = dictionary.messages

    if not isinstance(message, hl7.Message):
        raise Exception('Cannot validate message which is not an instance of '
                        'class \'hl7.Message\'')

    # Count number of appearances of each segment in message
    segments_name = parser.get_segments_name_from_message(message)
    segments_name_count = Counter(segments_name)

    # Get the rules, and check rule
    segments_rule = messages[message.name]['segments']['segments']
    for segment_rule in segments_rule:
        count = segments_name_count.get(segments_rule['name'], 0)
        boundary = cardinality_rules[segment_rule['min'], segment_rule['max']]
        if not (boundary[0] <= count <= boundary[1]):
            raise Exception(
                'Number of {} segment should be in between {}-{}'.format(
                    segment_rule['name'], boundary[0], boundary))
    return True


def validate_segments(segments):
    """Validate structure of segments
    :rtype: bool
    """

    return True


def validate_fields(fields):
    """Validate structure of fields

    :rtype: bool
    """

    return True
