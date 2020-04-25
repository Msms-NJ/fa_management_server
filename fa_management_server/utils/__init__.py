# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint
from flask.views import MethodView
from flask_login import login_required
from collections import ChainMap
from .custom_json_encoder import CustomJsonEncoder


def response_common(error_code=1, error_message=None, res_data=None, **kwargs):
    """数据返回共通函数"""
    response_dict = {
        "error_code": error_code, "error_message": error_message, "data": res_data,
    }
    for (k, v) in kwargs.items():
        response_dict[str(k)] = v
    return jsonify(response_dict)


def register_base_api(blueprint: Blueprint, view, endpoint="basic", pk="id", pk_type="string", is_login_require=True):
    view_func = view.as_view(endpoint)
    if is_login_require:
        view_func = login_required(view_func)
    blueprint.add_url_rule("/", view_func=view_func,
                           methods=["GET", "POST"])
    blueprint.add_url_rule("/<%s:%s>" % (pk_type, pk),
                           view_func=view_func,
                           methods=["GET", "PUT", "DELETE"])
