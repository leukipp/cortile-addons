#!/usr/bin/env python3

import json


class Dict(dict):
    def __init__(self, *args: object, **kwargs: object):
        """
        Initialize a dot notation dictionary.
        This helper class is used globally to provide simplified dictionary
        access by using the dot notation for attribute setter and getter methods.

        :param args: Dictionary argument
        :param kwargs: Keyword arguments
        """
        super().__init__(*args, **kwargs)
        for arg in args:
            if not isinstance(arg, dict):
                continue
            for k, v in arg.items():
                if isinstance(v, dict):
                    self[k] = Dict(v)
                elif isinstance(v, list):
                    self[k] = [Dict(x) if isinstance(x, dict) else x for x in v]
                else:
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    @staticmethod
    def from_json(string: str) -> object:
        """
        Instantiate a dot notation dictionary from json string.

        :param string: Dictionary as json string

        :return: Dot notation dictionary instance
        """
        return Dict(json.loads(string))

    def __getattr__(self, key: str) -> object:
        """
        Get dot notation dictionary attribute.

        :param key: Dictionary attribute key

        :return: Dictionary attribute value
        """
        return self.__getitem__(key)

    def __setattr__(self, key: str, value: object) -> None:
        """
        Set dot notation dictionary attribute.

        :param attr: Dictionary attribute key
        :param attr: Dictionary attribute value
        """
        self.__setitem__(key, value)

    def __delattr__(self, key: str) -> None:
        """
        Delete dot notation dictionary attribute.

        :param attr: Dictionary attribute key
        """
        self.__delitem__(key)

    def __str__(self) -> str:
        """
        Serialize dot notation dictionary as string.

        :return: Dictionary as json string
        """
        return json.dumps(self, indent=2)
