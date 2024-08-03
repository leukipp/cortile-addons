#!/usr/bin/env python3

import json


class Dict(dict):
    def __init__(self, *args, **kwargs):
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
    def from_json(str):
        return Dict(json.loads(str))

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __delattr__(self, item):
        self.__delitem__(item)

    def __str__(self):
        return self.str(self.__class__.__name__)

    def str(self, name):
        return f'{name}({", ".join(f"{k}={v}" for k, v in self.items())})'
