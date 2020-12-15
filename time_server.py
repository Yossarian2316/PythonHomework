from wsgiref.util import setup_testing_defaults, request_uri, shift_path_info
from wsgiref.simple_server import make_server
from datetime import datetime, timezone
import pytz
import json
from dateutil import parser


# Я написал  функцию tz_validator тк почему-то
# pytz_convert.validate_tz_name(tz_arg) выдает false для "одиночных" тайм зон
# Например:
# print(pytz_convert.validate_tz_name('Iran'))
# print(pytz_convert.validate_tz_name('Egypt'))
# print(pytz_convert.validate_tz_name('Cuba'))


def tz_validator(_timezone):
    tzlist = []
    for tz in pytz.all_timezones:
        tzlist.append(tz)
    for tz in tzlist:
        if tz == _timezone:
            return True
    return False


def get_response_handle(url, uri):
    status = '200 OK'

    headers = [('Content-type', 'text/plain; charset=utf-8')]
    if uri == '':
        response = str(datetime.now(timezone.utc).time())
    else:
        if len(url.split('/')) == 4:
            tz_arg = url.split('/')[3]
        else:
            tz_arg = url.split('/')[3] + '/' + url.split('/')[4]


        print(tz_arg)

        if tz_validator(tz_arg):
            tz = pytz.timezone(tz_arg)
            response = str(datetime.now(tz))[11:19]
        else:
            response = ''
            status = '400 Bad Request'
    return headers, status, response


def timezone_converter(input_dt, current_tz='UTC', target_tz='Iran'):
    current_tz = pytz.timezone(current_tz)
    target_tz = pytz.timezone(target_tz)
    target_dt = current_tz.localize(input_dt).astimezone(target_tz)
    return str(target_tz.normalize(target_dt))[:-6]


def convert(request_body):
    status = '200 OK'

    if tz_validator(request_body['target_tz']):
        response = timezone_converter(parser.parse(request_body['date']['date']),
                                      request_body['date']['tz'],
                                      request_body['target_tz'])
    else:
        response = '400 Bad Request'
        status = '400 Bad Request'

    return status, response


def date_difference(request_body):
    status = '200 OK'

    if not tz_validator(request_body['first_tz']) or tz_validator('second_tz'):
        status = '400 Bad Request'
        response = ['400 Bad Request']
        return status, response

    first_date = parser.parse(request_body['first_date'])
    first_tz = pytz.timezone(request_body['first_tz'])

    second_date = parser.parse(request_body['second_date'])
    second_tz = pytz.timezone(request_body['second_tz'])

    first = first_tz.localize(first_date)
    second = second_tz.localize(second_date)

    response = [str((first - second).total_seconds())]

    return status, response


def post_response_handle(url, env):
    status = '400 Bad Request'

    headers = [('Content-type', 'application/json; charset=utf-8')]
    response = ['400 Bad Request']

    api_type = url.split('/')[-1]

    request_body = json.loads(env['wsgi.input']
                              .read1()
                              .decode('utf-8')
                              .replace("\\", '')
                              [1:-1])

    if api_type == 'convert':
        status, response = convert(request_body)
        return headers, status, response

    if api_type == 'datediff':
        status, response = date_difference(request_body)
        return headers, status, response

    return headers, status, response


def handle_request(env, start_response):
    setup_testing_defaults(env)

    request_method = env['REQUEST_METHOD']
    url = request_uri(env)#строка запроса полностью
    uri = shift_path_info(env)#первая секция запроса после порта

    status = '200 OK'

    if request_method == 'GET':
        headers, status, response = get_response_handle(url, uri)

    if request_method == 'POST':
        headers, status, response = post_response_handle(url, env)

    start_response(status, headers)
    response = [x.encode('utf-8') for x in response]
    return response#


with make_server('', 8080, handle_request) as server:
    print("Serving on http://localhost:8080/")
    server.serve_forever()
