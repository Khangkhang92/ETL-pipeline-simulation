HTTP_STATUS_CODES = {
    100: ("Continue."),
    101: ("Switching Protocols."),
    102: ("Processing."),
    200: ("OK."),
    201: ("Created."),
    202: ("Accepted."),
    203: ("Non Authoritative Information."),
    204: ("No Content."),
    205: ("Reset Content."),
    206: ("Partial Content."),
    207: ("Multi Status."),
    226: ("IM Used."),  # see RFC 3229
    300: ("Multiple Choices."),
    301: ("Moved Permanently."),
    302: ("Found."),
    303: ("See Other."),
    304: ("Not Modified."),
    305: ("Use Proxy."),
    307: ("Temporary Redirect."),
    400: ("Bad Request."),
    401: ("Unauthorized."),
    402: ("Payment Required."),  # unused
    403: ("Forbidden."),
    404: ("Not Found."),
    405: ("Method Not Allowed."),
    406: ("Not Acceptable."),
    407: ("Proxy Authentication Required."),
    408: ("Request Timeout."),
    409: ("Conflict."),
    410: ("Gone."),
    411: ("Length Required."),
    412: ("Precondition Failed."),
    413: ("Request Entity Too Large."),
    414: ("Request URI Too Long."),
    415: ("Unsupported Media Type."),
    416: ("Requested Range Not Satisfiable."),
    417: ("Expectation Failed."),
    418: ("I'm a teapot."),  # see RFC 2324
    422: ("Unprocessable Entity."),
    423: ("Locked."),
    424: ("Failed Dependency."),
    426: ("Upgrade Required."),
    428: ("Precondition Required."),  # see RFC 6585
    429: ("Too Many Requests."),
    431: ("Request Header Fields Too Large."),
    449: ("Retry With."),  # proprietary MS extension
    500: ("Internal Server Error."),
    501: ("Not Implemented."),
    502: ("Bad Gateway."),
    503: ("Service Unavailable."),
    504: ("Gateway Timeout."),
    505: ("HTTP Version Not Supported."),
    507: ("Insufficient Storage."),
    510: ("Not Extended."),
}

HTTP_100_CONTINUE = {}
HTTP_101_SWITCHING_PROTOCOLS = {}
HTTP_200_OK = {}
HTTP_201_CREATED = {}
HTTP_202_ACCEPTED = {}
HTTP_203_NON_AUTHORITATIVE_INFORMATION = {}
HTTP_204_NO_CONTENT = {}
HTTP_205_RESET_CONTENT = {}
HTTP_206_PARTIAL_CONTENT = {}
HTTP_300_MULTIPLE_CHOICES = {}
HTTP_301_MOVED_PERMANENTLY = {}
HTTP_302_FOUND = {}
HTTP_303_SEE_OTHER = {}
HTTP_304_NOT_MODIFIED = {}
HTTP_305_USE_PROXY = {}
HTTP_306_RESERVED = {}
HTTP_307_TEMPORARY_REDIRECT = {}

HTTP_400_BAD_REQUEST = {
    400000: ("{}"),
    400001: ("Content-Type in request header is not 'src/json'!"),
    400002: ("Missing field in request!"),
    400003: ("Duplicated metadata"),
    400004: ("Metadata does not exist"),
    400005: ("Invalid param {0}"),
    400006: ("Value of param {0} has already existed"),
    400007: ("Arguments validation error"),
    400008: ("Parameter '{0}' is invalid"),
    400009: ("Database '{0}' does not exist"),
    400010: ("Database '{0}' is not supported"),
    400011: ("Filter field '{0}' is invalid"),
    400012: ("Error while casting field '{0}' to '{1}'"),
    400013: ("Data type '{0}' is not supported"),
    400014: ("Account not found"),
    400015: ("{} has already existed"),
    400016: ("Parameter {} in properties is required"),
    400017: ("Parameter {} is not allowed to search regex"),
    400018: ("Parameter {} is not a json string"),
    400019: ("Parameter {} is wrong format"),
    400020: ("{} object does not exist"),
    400021: ("user does not exist or has been activated"),
    400022: ("This email address is already used as a username"),
    400023: ("can't find verification record or Invalid token"),
    400024: ("can't commit a new record"),
    400025: ("can't create a new object"),
    400026: ("can't update records"),
    400027: ("User does not exist or has been deactivated"),
    400028: ("Unauthenticated user"),
    400029: ("User has been deleted"),
    400030: ("WatchList is empty"),
    400031: ("nothing added to watchlist"),
    400032: ("nothing add to watch list"),
    400033: ("nothing to delete watch list"),
    400034: ("resistance or support must greater than 0"),
    400035: ("This stock can't be predicted because lack of data"),
}

HTTP_401_UNAUTHORIZED = {
    401000: ("This email is not registered!"),
    401001: ("Authentication Failed: Wrong login name or password."),
    401002: ("JWT Token Invalid"),
    401003: ("Your link has expired"),
    401004: ("Refresh token is expired"),
    401005: ("Access token is expired"),
    401006: ("Unauthoried"),
}

HTTP_403_FORBIDDEN = {403000: ("{}"), 403001: ("Access denied!")}

HTTP_404_NOT_FOUND = {
    404001: ("File or folder does not exist!"),
    404002: ("Missing required fields"),
}
HTTP_405_METHOD_NOT_ALLOWED = {}
HTTP_406_NOT_ACCEPTABLE = {}
HTTP_407_PROXY_AUTHENTICATION_REQUIRED = {}
HTTP_408_REQUEST_TIMEOUT = {}
HTTP_409_CONFLICT = {}
HTTP_410_GONE = {}
HTTP_411_LENGTH_REQUIRED = {}
HTTP_412_PRECONDITION_FAILED = {}
HTTP_413_REQUEST_ENTITY_TOO_LARGE = {}
HTTP_414_REQUEST_URI_TOO_LONG = {}
HTTP_415_UNSUPPORTED_MEDIA_TYPE = {}
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE = {}
HTTP_417_EXPECTATION_FAILED = {}

HTTP_422_UNPROCESSABLE_ENTITY = {
    422001: ("Rule name: {0} already exists"),
    422002: ("Metadata: {0} - {1} already exists"),
    422003: ("Language: {0} already exists"),
}

HTTP_428_PRECONDITION_REQUIRED = {}
HTTP_429_TOO_MANY_REQUESTS = {
    429001: ("Too many requests"),
}
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = {}

HTTP_500_INTERNAL_SERVER_ERROR = {
    500001: ("Internal server error"),
    500002: ("File does not exist"),
    500003: ("Redis connection error"),
}

HTTP_501_NOT_IMPLEMENTED = {}
HTTP_502_BAD_GATEWAY = {}
HTTP_503_SERVICE_UNAVAILABLE = {}
HTTP_504_GATEWAY_TIMEOUT = {}
HTTP_505_HTTP_VERSION_NOT_SUPPORTED = {}
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = {}
