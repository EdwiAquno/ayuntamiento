from flask import Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(404)
def page_error_not_found(e):
    return render_template('error/404.html'), 404




@error_pages.app_errorhandler(403)
def page_forbidden(e):
    return render_template('error/403.html'), 403




@error_pages.app_errorhandler(500)
def page_internal_server_error(e):
    return render_template('error/500.html'), 500



@error_pages.app_errorhandler(401)
def page_unauthorized(e):
    return render_template('error/401.html'), 401
