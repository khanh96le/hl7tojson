# -*- coding: utf-8 -*-
import pickle
from os.path import dirname

from hl7tojson.utils.singleton import Singleton

SUPPORTED_VERSIONS = {'27'}
FILE_PATH = dirname(__file__)


@Singleton
class Dictionary:
    """Load data from file and save them to a singleton instance

    Usage::

        dictionary = Dictionary.Instance()
        dictionary.version
        >> 27

    """

    def __init__(self, version='27'):
        """Load a specify HL7 data version

        :param version: For now, only support version 2.7
        """

        if version not in SUPPORTED_VERSIONS:
            raise Exception('This version is not supported. Supporting {}'
                            ''.format(SUPPORTED_VERSIONS))

        self.version = version

        with open('{}/data/{}/fields.pickle'.format(FILE_PATH, version)) as f:
            self.fields = pickle.load(f)

        with open('{}/data/{}/messages.pickle'.format(FILE_PATH, version)) as f:
            self.messages = pickle.load(f)

        with open('{}/data/{}/segments.pickle'.format(FILE_PATH, version)) as f:
            self.segments = pickle.load(f)

        if not all([self.fields, self.messages, self.segments]):
            raise Exception('Some errors occurred during the loading '
                            'dictionary process')
