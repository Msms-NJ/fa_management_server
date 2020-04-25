from flask import Blueprint, jsonify
from jsonschema import ValidationError
from sqlalchemy.exc import DatabaseError

from ..utils import response_common

blueprint = Blueprint("errors", __name__)


@blueprint.app_errorhandler(500)
def server_error(error):
    return response_common(1, "Server Error", None), 404


@blueprint.app_errorhandler(404)
def handle_not_found_error(error):
    return response_common(1, "Not Found", None), 404


@blueprint.app_errorhandler(DatabaseError)
def handler_db_error(error: DatabaseError):
    return response_common(1, error.args, None), 500


@blueprint.app_errorhandler(ValidationError)
def handler_json_validate(error: ValidationError):
    """提交的JSON数据验证出错返回对应的错误信息"""
    res_message = None
    if error.validator == "required":
        res_message = "字段 %s 为必填项" % error.validator_value

    if error.validator == "minimum":
        res_message = "最小值不能小于 %d " % error.validator_value

    if error.validator == "maximum":
        res_message = "最大值不能大于 %d " % error.validator_value

    if error.validator == "format":
        if error.validator_value == "email":
            res_message = "字段 %s 不是合法的邮件格式" % error.instance

    if error.validator == "enum":
        res_message = "字段 %s 必须要是以下内容 %s" % (error.instance, error.validator_value)

    return response_common(1, error_message=res_message or error.message, res_data=None)

