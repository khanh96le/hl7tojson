# -*- coding: utf-8 -*-
import textwrap

import hl7

from hl7tojson.dictionary import Dictionary
from hl7tojson.exceptions import ParserError

dictionary = Dictionary.Instance()


def parse(message):
    try:
        sequence = parse_hl7_message(message)
        sequence.name = '{}_{}'.format(
            sequence[0][9][0][0], sequence[0][9][0][1])
    except Exception:
        raise ParserError('Cannot parse this message. Please make sure '
                          'the input is HL7 message.')
    return sequence


def get_segments_name_from_message(message):
    """Get list segments name from a message

    :param: message - instance of :py:class:`hl7.Message`
    :rtype: list
    """

    if not isinstance(message, hl7.Message):
        pass

    return [segment[0][0] for segment in message]


# def parse(message):
#     sequence = parse_hl7_message(message)
#     if not validate_segments(sequence):
#         raise Exception('The message is invalid')
#
#     sequence_with_description = update_description(0, sequence)
#     data = hl7_message_to_dict(sequence_with_description)
#     return data


def parse_hl7_message(message):
    """Parse the raw hl7 message to list of segments"""

    message = textwrap.dedent(message)
    h = hl7.parse(message)
    return h


def validate_segments(message):
    """Check if a parsed message containing legal segments"""

    if not isinstance(message, hl7.Message):
        raise Exception('The message should be an instance of hl7.Message')

    message_type = '{}_{}'.format(message[0][9][0][0], message[0][9][0][1])
    allow_segments = [
        segment['name']
        for segment in dictionary.messages[str(message_type)]['segments']['segments']
    ]
    actual_segments = [str(segment[0]) for segment in message]
    return set(actual_segments) < set(allow_segments)


def update_description(idx, sequence, **kwargs):
    """Update description for each sequence"""

    if isinstance(sequence, hl7.Message):
        message_type = '{}_{}'.format(
            sequence[0][9][0][0], sequence[0][9][0][1])
        sequence.desc = dictionary.messages[message_type]['desc']
        sequence.name = dictionary.messages[message_type]['name']
    elif isinstance(sequence, hl7.Segment):
        segment_type = str(sequence[0])
        sequence.desc = dictionary.segments[segment_type]['desc']
    elif isinstance(sequence, hl7.Field):
        if idx == 0:
            return
        segment_type = str(kwargs['parent'][0])
        sequence.desc = dictionary.segments[segment_type]['fields'][idx - 1]['desc']
        sequence.datatype = dictionary.segments[segment_type]['fields'][idx - 1]['datatype']
    elif isinstance(sequence, hl7.Repetition):
        field = kwargs['parent']
        sequence.desc = field.desc
        sequence.datatype = field.datatype
    elif isinstance(sequence, hl7.Component):
        field = kwargs['parent']
        if dictionary.fields[field.datatype]['subfields']:
            description = dictionary.fields[field.datatype]['subfields'][idx]['desc']
            datatype = dictionary.fields[field.datatype]['subfields'][idx]['datatype']
        else:
            description = dictionary.fields[field.datatype]['desc']
            datatype = field.datatype
        sequence.desc = description
        sequence.datatype = datatype

    if type(sequence) in [hl7.Message, hl7.Segment, hl7.Field, hl7.Repetition]:
        for idx, sub_sequence in enumerate(sequence):
            update_description(idx, sub_sequence, parent=sequence)

    return sequence


def hl7_message_to_dict(message):
    message_dict = {
        'info': _get_message_info(message),
        'segments': _get_segments_data(message)
    }
    return message_dict


def _get_message_info(message):
    return {
        'message_version': dictionary.version,
        'message_type': message.name,
        'message_description': message.desc,
    }


def _get_segments_data(message):
    segments_data = []
    for segment in message:
        segment_dict = {
            'type': segment[0][0],
            'description': segment.desc,
            'fields': _get_fields_data(segment)
        }
        segments_data.append(segment_dict)
    return segments_data


def _get_fields_data(segment):
    fields_data = []
    for idx, field in enumerate(segment):
        if idx == 0:
            continue

        if not str(field):
            continue

        field_dict = {
            'id': idx,
            'description': field.desc,
            'data': str(field),
            'repetitions': _get_repetitions_data(field)
        }
        fields_data.append(field_dict)
    return fields_data


def _get_repetitions_data(field):
    repetitions_data = []
    if not isinstance(field[0], hl7.Repetition):
        return repetitions_data

    for idx, repetition in enumerate(field):
        repetition_dict = {
            'description': repetition.desc,
            'data': str(repetition),
            'components': _get_components_data(repetition)
        }
        repetitions_data.append(repetition_dict)
    return repetitions_data


def _get_components_data(repetition):
    components_data = []
    if not isinstance(repetition[0], hl7.Component):
        return components_data

    for idx, component in enumerate(repetition):
        if not str(component):
            continue

        component_dict = {
            'id': idx + 1,
            'description': component.desc,
            'data': str(component)
        }
        components_data.append(component_dict)
    return components_data
