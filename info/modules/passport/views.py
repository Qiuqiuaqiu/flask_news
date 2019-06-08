from flask import request, abort, current_app, make_response

from info import redis_store, constants
from info.modules.passport import passport_blu
from info.utils.captcha.captcha import captcha



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
