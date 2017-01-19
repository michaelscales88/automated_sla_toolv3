from dateutil.parser import parse


def valid_dt(date_string):
    validated_dt = False
    try:
        validated_dt = parse(date_string, ignoretz=True)
    except ValueError:
        pass
    return validated_dt

