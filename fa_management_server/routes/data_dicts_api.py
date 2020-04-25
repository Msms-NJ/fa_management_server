# -*- coding: utf-8 -*-
"""Users api."""
from flask import Blueprint, json, jsonify
from flask.views import MethodView
from flask_login import login_required

from ..models import DataDict
from ..utils import CustomJsonEncoder, register_base_api

blueprint = Blueprint("data_dicts", __name__, url_prefix="/data-dicts")

schema = {
    "type": "object",
    "properties": {
        "dict_key": {"type": "string"},
        "dict_value": {"type": "string"},
        "dict_label": {"type": "string"},
        "dict_description": {"type": "string"},
        "dict_type": {"type": "string"}
    },
    "required": ["dict_key", "dict_value", "dict_type"]
}


class DataDictApi(MethodView):
    """数据字典基础REST接口"""

    # noinspection PyMethodMayBeStatic
    def get(self, id=None):
        """获取数据字典信息，如果有ID获取指定数据字典信息"""
        if id is None:
            users = DataDict.query.all()
            return jsonify(json.dumps(users, cls=CustomJsonEncoder))
        user = DataDict.get_by_id(id)
        return jsonify(user)

    def post(self):
        """新增数据字典信息接口"""
        pass

    # noinspection PyMethodMayBeStatic
    def delete(self, id=None):
        """删除数据字典信息接口"""
        if id is None:
            return "", 200
        data_dict = DataDict.get_by_id(id)
        if data_dict is not None:
            data_dict.delete()
        return "", 200

    def put(self, id=None):
        """更新用户信息接口"""
        pass


register_base_api(blueprint, DataDictApi)

