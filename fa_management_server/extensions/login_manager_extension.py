# -*- coding: utf-8 -*-

import jwt
from flask import current_app, jsonify
from flask_login import LoginManager

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """
    加载当前登录用户信息
    @param user_id:
    @return:
    """
    from ..models import User

    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify("unauthorized"), 401


@login_manager.request_loader
def load_user_from_request(request):
    """
    通过当前请求Header中的Authorization获取登录账户信息
    @param request:
    @return:
    """
    token = request.headers.get("Authorization")
    if token is None:
        token = request.args.get("token")
    try:
        if token is not None:
            from ..models import User
            user_map = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user = User.get_by_id(user_map["user"])
            if user is not None:
                return user
    except jwt.DecodeError as error:
        pass
    except jwt.ExpiredSignatureError as error:
        pass
    return None

# @login_manager.token_loader
# def token_loader_user(token):
#   print(token)
