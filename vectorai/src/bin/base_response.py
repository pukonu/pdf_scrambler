import json
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.middleware.csrf import get_token
from src.bin.lib import empty


class BaseResponse(object):
    STATUS_REMARK_OK = "OK"
    STATUS_REMARK_WARNING = "WARNING"
    STATUS_REMARK_ERROR = "ERROR"

    STYLE_GENERIC = "info"
    STYLE_SUCCESS = "success"
    STYLE_WARNING = "warning"
    STYLE_ERROR = "danger"

    RESPONSE_ERROR = "error"
    RESPONSE_WARNING = "warning"
    RESPONSE_SUCCESS = "success"

    METHOD_LOGIN = "login"
    METHOD_NEW = "new"
    METHOD_UPDATE = "update"
    METHOD_RETRIEVE = "retrieve"
    METHOD_VIEW_MAIN = "view"
    METHOD_VIEW_STATIC = "_vs"
    METHOD_VIEW_INSTANCE = "_vi"
    METHOD_VIEW_MODAL = "_p"
    METHOD_VIEW_TABLE = "_vt"
    METHOD_TABLE = "table"
    METHOD_DELETE = "delete"
    METHOD_VIEW_DELETE = "_vd"
    METHOD_OPTIONS_AJAX = "options-ajax"
    METHOD_SEARCH = "search"
    METHOD_OPTIONS_STATIC = "options-static"
    METHOD_LINKS = "links"
    METHOD_COUNT = "count"
    METHOD_META = "meta"
    METHOD_PDF = "pdf"
    METHOD_AUTHENTICATE = "authenticate"
    METHOD_MISC = "miscellaneous"
    METHOD_BLANK = "blank"

    MESSAGE_AUTH_GRANTED = _("Authorization granted")
    MESSAGE_LOGIN_SUCCESS = _("Login was successful")
    MESSAGE_SUCCESS = _("Your entry was successful")
    MESSAGE_SUCCESS_UPDATE = _("Your update was successful")
    MESSAGE_SUCCESS_RETRIEVAL = _("Retrieved successful")
    MESSAGE_DELETE = _("Deleted successfully")

    MALFORMED_URL = 404, _("Malformed URL called by end-user")
    GROUP_KEY_ERROR = 405, _("Group key index error. Please contact your system administrator")
    POSSIBLE_HACK = 403, _("Possible malicious access, this call has been logged")
    GET_EXCEPTION = 404, _("Uncaught error in get call, contact system administrator")
    GET_EXCEPTION_UNDEFINED_AJAX = 405, _("Undefined ajax search function in main program")
    GET_EXCEPTION_UNDEFINED_ATTRIBUTE = 405, _("Filter attribute error while querying data")
    POST_EXCEPTION = 400, _("Uncaught error in post call, contact system administrator")
    MULTIPLE_OBJECTS_RETURNED = 500, _("Returned multiple objects where one object was expected, critical error. "
                                       "Please contact your system administrator")
    PERMISSION_ERROR = 403, _("General permission error, contact system administrator to grant permissions for "
                              "the module you have attempted to access")
    LOGIN_ERROR = 400, _("User and password doesn't exist in our record")
    AUTHORIZATION_BEARER_ERROR = 401, _("No authorization bearer secret passed in header")
    AUTHORIZATION_TOKEN_ERROR = 401, _("No authorization token passed in header or token has expired")
    AUTHORIZATION_COOKIE_ERROR = 401, _("CSRF token failure")

    PERMISSION_ALL = "all"
    PERMISSION_MANAGE = "manage"
    PERMISSION_CREATE = "create"
    PERMISSION_UPDATE = "update"
    PERMISSION_DELETE = "delete"
    PERMISSION_VIEW = "view"
    PERMISSION_DELETE_CONDITIONAL = "delete_conditional"
    PERMISSION_DELETE_MINE = "delete_mine"
    PERMISSION_MANAGE_CONDITIONAL = "manage_conditional"
    PERMISSION_MANAGE_MINE = "manage_mine"
    PERMISSION_RETRIEVE_CONDITIONAL = "view_conditional"
    PERMISSION_RETRIEVE_MINE = "view_mine"
    PERMISSION_RETRIEVE_ALL = "view_all"
    PERMISSION_NO_AUTH = "no_authentication"
    PERMISSION_NONE = None
    PERMISSION_SUPER_ADMIN = "super_admin"

    dump = {}
    _status_remark = None
    _warning = False
    _success = False
    _error = False
    _error_detail = None
    _route = None
    _response = None
    _method = None
    _message = None
    _delay = None
    _js_command = None
    _style = "info"
    _error_code = None
    _error_code_description = None
    _data = None
    _results = None
    _template = None
    _html_data = None
    _misc = {}

    _module = None
    _request = None
    _is_authenticated = True

    def __init__(self, message=None, method=None, response=None, route=None, js_command=None,
                 style=None, template=None, html_data=None, request=None):
        self._message = message
        self._method = method
        self._response = response
        self._route = route
        self._js_command = js_command
        self._style = style or BaseResponse.STYLE_GENERIC
        self._template = template
        self._html_data = html_data

        self._request = request

        if response is not None:
            if response == BaseResponse.RESPONSE_ERROR:
                self._status_remark = BaseResponse.STATUS_REMARK_ERROR
                self.error()

            elif response == BaseResponse.RESPONSE_WARNING:
                self._status_remark = BaseResponse.STATUS_REMARK_WARNING
                self.warning()

            else:
                self._status_remark = BaseResponse.STATUS_REMARK_OK
                self.success()

        else:
            self.success()
            self._status_remark = BaseResponse.STATUS_REMARK_OK

    def status_remark(self, status_remark):
        self.dump["status_remark"] = status_remark
        return self

    def warning(self):
        if empty(self._delay):
            self._delay = 5000

        self._style = BaseResponse.STYLE_WARNING
        self._warning = True
        return self

    def error(self):
        if empty(self._delay):
            self._delay = 25000

        self.status_remark(BaseResponse.STATUS_REMARK_ERROR)
        self._style = BaseResponse.STYLE_ERROR
        self._error = True
        return self

    def success(self):
        if empty(self._delay):
            self._delay = 3000

        if empty(self._message) and self._method == BaseResponse.METHOD_DELETE:
            self._message = BaseResponse.MESSAGE_DELETE

        elif empty(self._message) and \
                (self._method == BaseResponse.METHOD_RETRIEVE or self._method == BaseResponse.METHOD_TABLE):
            self._message = BaseResponse.MESSAGE_SUCCESS_RETRIEVAL

        elif empty(self._message) and self._method == BaseResponse.METHOD_UPDATE:
            self._message = BaseResponse.MESSAGE_SUCCESS_UPDATE

        elif empty(self._message) and self._method == BaseResponse.METHOD_NEW:
            self._message = BaseResponse.MESSAGE_SUCCESS

        elif empty(self._message) and self._method == BaseResponse.METHOD_LOGIN:
            self._message = BaseResponse.MESSAGE_LOGIN_SUCCESS

        self._success = True
        return self

    def js_command(self, js_command):
        self._js_command = js_command
        return self

    def route_to(self, route):
        self._route = route
        return self

    def message(self, message):
        self._message = message
        return self

    def style(self, style):
        self._style = style
        return self

    def error_code(self, error_code):
        self._error_code = error_code[0]
        self._error_code_description = error_code[1]
        return self

    def set_error_detail(self, error_detail):
        self._error_detail = error_detail
        return self

    def auth_guard(self, val):
        if not val:
            self.error()
            self._is_authenticated = False
        return self

    def append_data(self, data, **options):
        self._data = data

        try:
            self._results = options["results"]
        except KeyError:
            pass

        try:
            self._data['extras'] = options["extras"]
        except KeyError:
            pass

        try:
            self._misc = options["misc"]
        except KeyError:
            pass

        return self

    def delay(self, delay):
        self._delay = delay
        return self

    def data_to_dict(self):
        try:
            self._data = json.loads(self._data)
        except (TypeError, ValueError):
            pass

        return self

    def render(self):
        self.data_to_dict()
        self.dump = {
            "statusRemark": self._status_remark,
            "status": {
                "warning": self._warning,
                "error": self._error,
                "success": self._success,
            },
            "message": self._message,
            "method": self._method,
            "delay": self._delay,
            "jsCommand": self._js_command,
            "style": self._style,
            "route": self._route,
            "systemError": {
                "code": self._error_code,
                "codeDescription": self._error_code_description,
                "errorDetail": self._error_detail,
            },
            "data": self._data,
            "results": self._results,
            "module": self._module,
            "i18n": "en-gb",
            "misc": self._misc,
        }
        return self

    def response_html(self):
        from django.shortcuts import render

        status_code = 200

        # clean up error message
        try:
            if self.dump["status"]["error"] is True:
                if type(self.dump["message"]) == tuple:
                    status_code = self.dump["message"][0]
                    self.dump["message"] = self.dump["message"][1]
                else:
                    status_code = 400
        except KeyError:
            status_code = 400

        # continue with rendering
        if self._html_data:
            if self._template:
                return render(self._request, self._template, self._html_data)

            else:
                return HttpResponse(self._html_data["msg"])

        else:
            if not self._is_authenticated:
                response = HttpResponse(self.response_json(), content_type='application/json')
                response["Authorization"] = "not_authorized"
                response["Access-Control-Expose-Headers"] = "Authorization"

            else:
                response = HttpResponse(self.response_json(), content_type='application/json')

            response.status_code = status_code

            return response

    def response_json(self):
        return json.dumps(self.dump, cls=DjangoJSONEncoder)

    def response_raw(self):
        return self.dump

    def pre_response_delete(self, instance, message=None):
        fqn = instance.get_fqn()

        if message is None:
            if settings.DEBUG:
                message = _("You are about to delete <strong>%s</strong> from your records. "
                            "How do you want to proceed?") % fqn

            else:
                message = _("You are about to delete <strong>'%s'</strong> from your records. "
                            "How do you want to proceed?") % fqn

        self.warning()
        self._success = False
        self._method = BaseResponse.METHOD_DELETE
        self._message = message
        return self

    # authentication
    def get_method_default_permission(self, method):

        if method is None:
            method = ""

        if method == self.METHOD_RETRIEVE or method == self.METHOD_TABLE or method == self.METHOD_OPTIONS_STATIC \
                or method == self.METHOD_OPTIONS_AJAX:
            return self.PERMISSION_VIEW

        elif method == self.METHOD_DELETE:
            return self.PERMISSION_DELETE

        elif method == self.METHOD_NEW:
            return self.PERMISSION_CREATE

        elif method == self.METHOD_UPDATE:
            return self.PERMISSION_UPDATE

        else:
            return None
