# -*- coding: utf-8 -*-
from flask import json

from ..models import Role, User


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if any([isinstance(obj, User), isinstance(obj, Role)]):
            return obj.__str__
        else:
            return json.JSONEncoder.default(self, obj)
