# -*- coding: utf-8 -*-


class ParserError(Exception):
    def __init__(self, message):
        self.message = message
