# -*- coding: utf-8 -*-
"""Role restful api."""

from flask import Blueprint, json, jsonify, request
from flask.views import MethodView
from flask_login import login_required
from jsonschema import validate, draft7_format_checker

from ..utils import response_common, register_base_api
from ..models import Role

blueprint = Blueprint("roles", __name__, url_prefix="/roles")

# 定义输入数据格式
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "data_scope": {"type": "integer", "enum": [
            Role.DATA_SCOPE_DEFAULT, Role.DATA_SCOPE_SELF, Role.DATA_SCOPE_OFFICE, Role.DATA_SCOPE_ALL
        ]},
        "web_menus": {"type": "array", "items": {"type": "string"}},
        "remarks": {"type": "string"}
    },
    "required": ["name", "data_scope"]
}

multi_delete_schema = {
    "type": "array",
    "items": {"type": "string"},
}


def get_request_role():
    """登录、注册功能的共用函数，用来从json中获取账号，密码信息"""
    if request.is_json:
        req_json = request.get_json()
        validate(instance=req_json, schema=schema, format_checker=draft7_format_checker)
        if "id" in req_json:
            req_json.pop("id")
        return req_json
    return None


class RoleApi(MethodView):
    """
    用户角色增、删、改、查接口
    """

    # noinspection PyMethodMayBeStatic
    def get(self, id=None):
        if id is None:
            return response_common(
                0, "请求成功", Role.all(),
                success=True, total=Role.query.count(),
            )
        else:
            role = Role.get_by_id(id)
            if role is not None:
                return response_common(0, "请求成功", role)
            else:
                return response_common(1, "角色不存在", None)

    # noinspection PyMethodMayBeStatic
    def post(self):
        req_json = get_request_role()
        name = req_json["name"]
        if Role.query.filter_by(name=name).first() is not None:
            return response_common(1, "角色名称 %s 已经存在" % name, None)
        if req_json is not None:
            role = Role.create_from_json(req_json)
            return response_common(0, "请求成功", role)
        else:
            return response_common(1, "解析JSON数据出错")

    # noinspection PyMethodMayBeStatic
    def put(self, id):
        role = Role.get_by_id(id)
        if role is None:
            return response_common(1, "角色不存在，无法更新", None)
        role.update(get_request_role())
        return response_common(0, "请求成功", role)

    # noinspection PyMethodMayBeStatic
    def delete(self, id):
        role = Role.get_by_id(id)
        if role is not None:
            role.delete()
        return response_common(0, "请求成功")


register_base_api(blueprint, RoleApi)


@blueprint.route("/multi", methods=["DELETE"])
@login_required
def delete_multi_roles():
    """"批量删除用户角色接口"""
    print(request.get_json())
    return response_common(0, "请求成功")
