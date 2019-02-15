import json
import re
from django.utils.translation import gettext as _
from src.bin import dictionary


def form_meta(fields):
    tmp = []
    tmp2 = []
    for field in fields:
        tmp.append(''''%s': forms.TextInput(attrs={'placeholder': '', 'class': 'form-control'}),''' % field)
        tmp2.append(''''%s': "%s",''' % (field, field.title()))


def format_form_error(form):
    regex = re.compile("<[^<]+?>", re.IGNORECASE)
    ret = []
    for x in form.errors:
        label = form.fields[x].label
        data = "%s [%s]" % (form.errors[x], _(label))
        ret.append(regex.sub('', str(data)))

    return ret


def value_separator(value):
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US')
    return locale.format("%d", value, grouping=True)


def incr_meta(global_objects, value='META_ROW', step=10, reset=False):
    if reset:
        global_objects[value] = 0

    global_objects[value] += step
    return global_objects[value]


def number_choice(start=1, end=100, step=1, r_type=str, empty_string=None):

    objects = range(start, end+1)[::step]
    choice = []

    if empty_string:
        choice.append(('', empty_string))

    for obj in objects:
        choice.append((r_type(obj), r_type(obj)))

    return tuple(choice)


def month_choice():
    choice = (
        ('', _('Select a month')),
        ('1', _('January')),
        ('2', _('February')),
        ('3', _('March')),
        ('4', _('April')),
        ('5', _('May')),
        ('6', _('June')),
        ('7', _('July')),
        ('8', _('August')),
        ('9', _('September')),
        ('10', _('October')),
        ('11', _('November')),
        ('12', _('December')),
    )

    return choice


def given_year(start=1970, end=2048, extra=1):
    from datetime import datetime

    if end == 'now':
        end = int(datetime.now().year) + extra
    
    default = datetime.now().year
    choices = number_choice(start, end)
    
    return choices, default


def given_month():
    from datetime import datetime
    from src.bin.dictionary import Month
    
    current_month = datetime.now().month
    default = Month.month_name[current_month-1]
    choices = []
    
    for month in Month.month_name:
        choices.append((month, month),)
    
    return tuple(choices), default


def path_and_rename(instance, filename):
    import hashlib
    import datetime
    ext = '.' + filename.split('.')[-1]
    filename = hashlib.md5(instance.reference + str(datetime.datetime.now())).hexdigest() + ext
    return '/'.join(['shareware/dmc/hr/photos', filename])


def cert_path_and_rename(instance, filename):
    import hashlib
    import datetime
    ext = '.' + filename.split('.')[-1]
    filename = hashlib.md5(instance.profile.reference + str(datetime.datetime.now())).hexdigest() + ext
    return '/'.join(['shareware/dmc/hr/certificate', filename])


def get_thumb(path, version='128x128'):
    ext = '.' + path.split('.')[-1]
    filename = "".join(path.split('.')[:-1])
    return filename + '.' + version + ext


def drop_down(data, default=None, element_id=None, row=0):

    s = ''
    n = 0

    for instance in data:
        for x, y in instance.items():
            if str(default) == str(x):
                s += '''<option value="%s_%s" selected="selected">%s</option>''' % (n, x, y)
            else:
                s += '''<option value="%s_%s">%s</option>''' % (n, x, y)

            n += 1

    obj = '''<select id="{element_id}" name="{element_id}" class="form-control {element_id} pp-drop-down"
                data-row="{row}">
        {val}
    </select>'''.format(element_id=element_id, val=s, row=row)

    return obj


def response_success(route='', response=None, delay=1000, status=1, modal=False):
    res = dictionary.Defs().FormSuccess
    res['route'] = route
    res['delay'] = delay
    res['response'] = response if response is not None else res['response']
    res['status'] = status
    res['modal'] = str(modal).lower()

    return json.dumps(res)


def response_error(response, route=''):
    res = dictionary.Defs().FormError

    if type(response).__name__ == 'str' or type(response).__name__ == 'unicode':
        res['route'] = route
        res['response'] = response

    else:
        i = 1
        response_str = ""
        if response:
            for y in response:
                for x in y:
                    response_str += "%s. %s<br/>" % (str(i), x)
                    i += 1
        else:
            response_str = res['response']

        res['route'] = route
        res['response'] = response_str

    return json.dumps(res)


def response_generic(response, route=None, style="info", delay=None, command=None):
    res = dictionary.Defs().Info

    if type(response) == list:
        i = 1
        response_str = ""
        for y in response:
            for x in y:
                response_str += "%s. %s<br/>" % (str(i), x)
                i += 1

    else:
        response_str = str(response)

    res['route'] = route
    res['response'] = response_str
    res['style'] = style if style else res['style']
    res['delay'] = delay if delay else res['delay']
    res['command'] = command if command else res['command']

    return json.dumps(res)


def random_chars(size, chars=None):
    import random
    from string import ascii_uppercase, ascii_lowercase, digits
    from itertools import islice

    if chars == 'alphanumeric':
        chars = (ascii_lowercase + digits)
    elif chars == 'text':
        chars = ascii_lowercase
    elif chars == 'number':
        chars = digits
    else:
        chars = (ascii_uppercase + ascii_lowercase + digits)

    selection = iter(lambda: random.choice(chars), object())
    while True:
        yield ''.join(islice(selection, size))


def autocomplete_state(queryset=None, instance_var=None, url=None, element=None, token=1, theme='wit2', enclose=True):

    if instance_var is None or instance_var == []:
        json_object = ""

    elif token > 1:
        try:
            try:
                tmp = instance_var
            except (ValueError, AttributeError):
                tmp = ""

            if type(tmp) == str:
                m_objects = tmp.split(',')
            else:
                m_objects = []
                for m_object in tmp:
                    m_objects.append(m_object.id)

            arr = []
            for m_object in m_objects:
                r_object = queryset.get(id=m_object)
                arr.append('''{'id':'%s', 'name':"%s"}''' % (str(m_object), r_object))

            json_object = ''', prePopulate: [%s]''' % (','.join(arr)) if arr else ""

        except (ValueError, UnboundLocalError):
            json_object = ""

    else:
        try:
            json_object = ''', prePopulate: [{'id':'%s', 'name':'%s'}]''' % (str(instance_var.id), instance_var)

        except (ValueError, UnboundLocalError):
            json_object = ""

    if enclose:
        tag_open = "<script>"
        tag_close = "</script>"
    else:
        tag_open = tag_close = ""

    script = '''
    %s
    $(document).ready(function(){
        $('#%s').tokenInput('%s', {theme:'%s', tokenLimit:%s, hintText:'Start typing name' %s});
    });
    %s''' % (tag_open, element, url, theme, token, json_object, tag_close)

    return script


def mkdir_if_not_exists(path):
    import os

    directory = "/".join(path.split('/')[0:len(path.split('/'))-1])
    if not os.path.exists(directory):
        os.makedirs(directory)


def password_checker(password, min_strength=3, forbidden=list()):

    import re

    error = None

    password_strength = dict.fromkeys(['has_upper', 'has_lower', 'has_num', 'has_length'], False)

    # check against forbidden list
    if password in forbidden:
        error = _('Your password cannot be <b>"%s"</b>' % password)

    if len(password) >= 8:
        password_strength['has_length'] = True
    if re.search(r'[A-Z]', password):
        password_strength['has_upper'] = True
    if re.search(r'[a-z]', password):
        password_strength['has_lower'] = True
    if re.search(r'[0-9]', password):
        password_strength['has_num'] = True

    score = len([b for b in password_strength.values() if b])

    if score >= min_strength:
        return True, None
    else:
        return False, error


def encrypt_password(val):
    from django.conf import settings
    from hashlib import sha1, sha256

    if settings.PASSWORD_ENCRYPTION_METHOD == 'SHA256':
        return sha256(val).hexdigest()

    elif settings.PASSWORD_ENCRYPTION_METHOD == 'SHA1':
        return sha1(val).hexdigest()

    else:
        return val


def escape(value):
    from django.utils.html import escape as html_escape, strip_tags

    if value:
        value = html_escape(strip_tags(value))
    return value


def empty(value, strict=False):
    if (value is None or value == "" or value == 0) and strict:
        return True
    elif value is None or value == "":
        return True
    else:
        return False


def timesince(dt, default="just now"):
    from django.utils import timezone

    now = timezone.now()

    if dt > now:
        return _("time in future")

    diff = now - dt
    periods = (
        (diff.days/365, _("year"), _("years")),
        (diff.days/30, _("month"), _("months")),
        (diff.days/7, _("week"), _("weeks")),
        (diff.days, _("day"), _("days")),
        (diff.seconds/3600, _("hour"), _("hours")),
        (diff.seconds/60, _("minute"), _("minutes")),
        (diff.seconds, _("second"), _("seconds")),
    )
    for period, singular, plural in periods:
        if period and period > 1:
            return _("%d %s ago") % (period, singular if period == 1 else plural)

    return default


def month_iterator(backwards=6, forward=6):
    """
    This function iterate months from backward to forward based on the current date
    This function is only correct if the lagging or leading months are less than 28
    :param backwards:
    :param forward:
    :return:
    """

    from django.utils import timezone
    from datetime import timedelta, date

    today = timezone.now().date()
    mid_pivot_month = date(today.year, today.month, 15)

    i_date = mid_pivot_month - timedelta(days=(30.42 * backwards))
    end_date = mid_pivot_month + timedelta(days=(30.42 * forward))

    while i_date < end_date:
        yield {"y": i_date.year, "m": i_date.month}
        i_date += timedelta(days=30.42)


def date_range(backwards=6, forward=6):
    """
    This function return a tuple containing the backward and forward dates from an option.
    The backward date will start from day 1 and end date will be the last date of the given end month
    :param backwards:
    :param forward:
    :return:
    """
    from calendar import monthrange
    from django.utils import timezone
    from datetime import timedelta, date

    today = timezone.now().date()
    mid_pivot_month = date(today.year, today.month, 15)

    _sd = mid_pivot_month - timedelta(days=(30.42 * backwards))
    _ed = mid_pivot_month + timedelta(days=(30.42 * forward))

    start_date = date(_sd.year, _sd.month, 1)
    end_date = date(_ed.year, _ed.month, monthrange(_ed.year, _ed.month)[1])

    return start_date, end_date


def format_static_options(options):
    data = list()
    for option in options:
        data.append({
            "value": option[0],
            "label": option[1],
        })

    return data


def format_dynamic_options(model, model_manager, filters, label="name"):
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.utils import ProgrammingError

    data = list()
    try:
        queryset = getattr(model, model_manager).filter(**filters)
        for option in queryset:
            data.append({
                "value": option.pk,
                "label": getattr(option, label),
            })

    except (ObjectDoesNotExist, ProgrammingError):
        pass

    return data


def format_queryset_options(queryset, label="name"):
    data = list()
    for option in queryset:
        data.append({
            "value": option.pk,
            "label": getattr(option, label),
        })

    return data


def format_file_from_base64(request, attr):
    import base64
    from django.utils import timezone
    from django.core.files.base import ContentFile
    from src.bin.constants import MIME_TYPES

    file_format_lib = {"data:"+v["mime"]: v["extension"].replace(".", "") for v in MIME_TYPES}

    try:
        tmp_filename = str(timezone.now())
        file_content = json.loads(request.body)[attr]
        file_format, file_binary_string = file_content.split(';base64,')
        # ext = file_format.split('/')[-1]
        # print file_format.lower()
        ext = file_format_lib[file_format.lower()]
        return ContentFile(base64.b64decode(file_binary_string), name=tmp_filename + '.' + ext)

    except (ValueError, IndexError, KeyError, OSError, AttributeError, TypeError):
        return None


def inplace_file(request, instance, prop):
    file_object = format_file_from_base64(request, prop)

    print(file_object)

    thumbs = ['64x64', '128x128', '256x256', '512x512', '1024x1024']

    if file_object:
        # check if previous file exist and replace if so
        try:
            current_file = getattr(instance, prop)
            delete_photo_with_thumbs(current_file, thumbs)
        except AttributeError:
            pass
        setattr(instance, prop, file_object)


def delete_photo_with_thumbs(field_object, thumbs):
    import os
    from django.conf import settings

    try:
        file_name = field_object.url.split(".")[0]
        file_ext = field_object.url.split(".")[-1]

        for thumb in thumbs:
            file_url = "%s.%s.%s" % (file_name, thumb, file_ext)
            file_path = settings.BASE_DIR + file_url
            try:
                os.path.exists(file_path) and os.remove(file_path)
            except OSError:
                pass
    except (AttributeError, IndexError, TypeError, ValueError):
        pass


def get_http_headers(request):
    import re

    regex_http_ = re.compile(r'^HTTP_.+$')
    regex_content_type = re.compile(r'^CONTENT_TYPE$')
    # regex_content_length = re.compile(r'^CONTENT_LENGTH$')
    regex_authorization = re.compile(r'^AUTHORIZATION$')

    request_headers = dict()
    for header in request.META:
        if regex_http_.match(header) or regex_content_type.match(header) or regex_authorization.match(header):
            request_headers[header] = request.META[header]

    return request_headers


def safe_execute_expression(default, exception, expression):
    try:
        print(expression)
        exec(expression)
    except exception:
        return default


def decamelize(name, hyphenate=True):
    if hyphenate:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

    else:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_obj_by_key_from_arr(obj, key=None, val=None, return_key=None, default_value=None):
    for x in obj:
        try:
            _c = x[key].lower()
        except AttributeError:
            _c = None

            if empty(val) and empty(x[key]):
                return x[return_key]

        if _c == val.lower():
            return x[return_key]

    return default_value


def date_range_count(start, end, skip_days=list(), workdays=None, skip_dates=list()):
    from datetime import timedelta

    workdays = [0, 1, 2, 3, 4, 5, 6] if not workdays else workdays
    days = 0
    i = start

    while i <= end:
        weekday = i.weekday()
        if weekday in workdays and weekday not in skip_days and i not in skip_dates:
            days += 1

        i += timedelta(1)

    return days


def get_token(request):
    try:
        headers = dict((k.lower(), v) for k, v in get_http_headers(request).items())
        return headers["http_authorization"].split(" ")[1]

    except (IndexError, KeyError):
        return


def encrypt(value, encryption_mode="sha256"):
    import hashlib

    if encryption_mode is None:
        return value

    return getattr(hashlib, encryption_mode)(str(value).encode("utf8")).hexdigest()


def build_url(base, sub):
    return base.replace("subdomain", sub)
