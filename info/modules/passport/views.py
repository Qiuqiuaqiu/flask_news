import random
import re

from flask import request, abort, current_app, make_response, jsonify

from info import redis_store, constants
from info.libs.yuntongxun.sms import CCP
from info.modules.passport import passport_blu
from info.response_code import RET
from info.utils.captcha.captcha import captcha

@passport_blu.route("/sms_code",methons=["POST"])
def get_msg_code():
    dict_data = request.json
    modile, image_code, image_code_id = dict_data.get("modile"), dict_data.get("image_code"), dict_data.get(
        "image_code_id")
    if not all([modile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    if not re.match(r"1[35678]\d{9}", modile):
        return jsonify(erron=RET.PARAMERR, errmsg="手机号格式不正确")

    try:
        real_image_code = redis_store.get("ImageCodeId_" + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(erron=RET.DBERR, errmsg="数据库查询失败")

    if not real_image_code:
        return jsonify(erron=RET.NODATA, errmsg="图片验证码已过期")

    if image_code.upper() != real_image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码输入错误")

    sms_code_str = "%06d" % random.randint(0, 999999)
    result = CCP().send_template_sms(modile, [sms_code_str, 5], 1)
    if result != 0:
        return jsonify(errno=RET.THIRDERR, errmsg="第三方错误")
    try:
        redis_store.setex("sms_" + modile, constants.SMS_CODE_REDIS_EXPIRES, sms_code_str)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="手机验证码保存失败")

    return jsonify(errno=RET.OK, errmsg="发送成功")


@passport_blu.route("/image_code")
def get_image_code():

    image_code_id = request.args.get("imageCodeId")

    if not image_code_id:
        abort(404)

    _, text, image = captcha.generate_captcha()

    try:
        redis_store.setex("ImageCodeId"+image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)
    response = make_response(image)
    response.headers["Content-Type"] = "image/jpg"

    return response
