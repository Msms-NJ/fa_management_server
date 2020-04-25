# -*- coding: utf-8 -*-
"""Login api."""
import jwt
from flask import Blueprint, current_app, jsonify, request
from flask_login import login_required, login_user, logout_user

from ..models import User
from ..utils import response_common

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def get_request_data():
    """登录、注册功能的共用函数，用来从json中获取账号，密码信息"""
    if request.is_json:
        req = request.get_json()
        username = req.get("username", None)
        password = req.get("password", None)
        password_confirm = req.get("password_confirm", None)
        mobile = req.get("mobile", None)
        captcha = req.get("captcha", None)
        return username, password, password_confirm, mobile, captcha
    return None, None, None, None, None


@blueprint.route("/login/captcha", methods=["POST"])
def login_captcha():
    """手机号，手机验证码登录接口，请求数据为mobile，captcha"""
    *_, mobile, captcha = get_request_data()
    user = User.query.filter_by(mobile=mobile).first()
    return None


@blueprint.route("/login", methods=["POST"])
def login():
    """登录接口，请求数据为username，password"""
    username, password, *_ = get_request_data()
    if username is None:
        return response_common(1, "用户名不能为空")
    if password is None:
        return response_common(1, "用户密码不能为空")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return response_common(1, "用户%s不存在" % username)
    if user.check_password(password):
        token = jwt.encode(
            {"user": user.id}, current_app.config["SECRET_KEY"], algorithm="HS256"
        )
        return response_common(0, "登录成功", str(token, "utf-8"))
    else:
        return response_common(1, "密码错误，请输入正确的密码")


@blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    """注销接口"""
    logout_user()
    return response_common(0, "注销成功")


@blueprint.route("/register", methods=["POST"])
def register():
    """注册接口，用来注册账户信息"""
    username, password, password_confirm, mobile, captcha = get_request_data()
    if username is None or password is None or password_confirm is None:
        return response_common(1, "请输入正确的姓名、密码信息")
    if mobile is None:
        return response_common(1, "请输入手机号码")
    if captcha is None:
        return response_common(1, "请输入验证码")
    if password != password_confirm:
        return response_common(1, "密码和确认密码不正确，请重新输入")

    if User.query.filter_by(username=username).first() is not None:
        return response_common(1, "用户名%s已被使用，请重新输入" % username)

    if User.query.filter_by(mobile=mobile).first() is not None:
        return response_common(1, "手机号码%s已被使用，请重新输入" % mobile)

    user = User.create(username=username, password=password, mobile=mobile)
    return response_common(0, "用户%s注册成功" % username, user.serialize())


@blueprint.route("/wechat", methods=["POST"])
def wechat_auth():
    pass
