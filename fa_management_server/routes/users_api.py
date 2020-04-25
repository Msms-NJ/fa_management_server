# -*- coding: utf-8 -*-
"""Users api."""
from flask import Blueprint, json, jsonify
from flask.views import MethodView
from flask_login import current_user, login_required

from ..models import User
from ..utils import CustomJsonEncoder, register_base_api, response_common

blueprint = Blueprint("users", __name__, url_prefix="/users")


class UsersApi(MethodView):
    """登录用户基础REST接口"""

    decorators = [login_required]

    # noinspection PyMethodMayBeStatic
    def get(self, id=None):
        """获取用户信息，如果有ID获取单个用户信息"""
        if id is None:
            users = User.query.all()
            return jsonify(json.dumps(users, cls=CustomJsonEncoder))
        user = User.get_by_id(id)
        return response_common(0, "请求成功", user)

    def post(self):
        """新增用户信息接口"""
        pass

    # noinspection PyMethodMayBeStatic
    def delete(self, id=None):
        """删除用户信息接口"""
        user = User.get_by_id(id)
        if user is not None:
            user.delete()
        return response_common(0, "删除成功")

    def put(self, id=None):
        """更新用户信息接口"""
        pass


register_base_api(blueprint, UsersApi)


@blueprint.route("/current", methods=["GET"])
@login_required
def current():
    """获取当前登录用户"""
    return jsonify(
        id=current_user.id, email=current_user.email, username=current_user.username,
    )
