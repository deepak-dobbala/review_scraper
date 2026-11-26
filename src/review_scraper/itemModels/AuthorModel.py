from datetime import date
import re
# here regualar expressions are used for multiple  delimiter splits

import attrs

month_to_int = {
    'january' : 1,
    'february' : 2,
    'march' : 3,
    'april' : 4,
    'may' : 5,
    'june' : 6,
    'july' : 7,
    'august' : 8,
    'september' : 9,
    'october' : 10,
    'november' : 11,
    'december' : 12,
}

def parse_str_date(str_date):
    arr = re.split(r'[, ]+', str_date)
    month = month_to_int[arr[0].lower()]
    day = int(arr[1])
    year = int(arr[2])
    return date(year, month, day)

@attrs.define
class AuthorModelItem():
    author_name = attrs.field(type = str)
    author_dob = attrs.field(type = date, converter = parse_str_date)
    author_desc = attrs.field(type = str, default = "")