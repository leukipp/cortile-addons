#!/usr/bin/env python3

import json


class Dict(dict):
    def __init__(self, *args: object, **kwargs: object):
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
    def from_json(str: str) -> object:
        return Dict(json.loads(str))

    def __getattr__(self, attr: str) -> object:
        return self.__getitem__(attr)

    def __setattr__(self, key: str, value: object) -> None:
        self.__setitem__(key, value)

    def __delattr__(self, item: str) -> None:
        self.__delitem__(item)

    def __str__(self) -> str:
        return json.dumps(self, indent=2)
