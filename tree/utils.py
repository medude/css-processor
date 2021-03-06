def is_key_val(string):
    return ":" in string


def split_key_val(string):
    key_val = string.split(":")
    return {
        "key": key_val[0],
        "val": key_val[1][1:]
    }


def ends_with(string, last_char):
    return string[len(string) - 1:] == last_char


def strip_last_char(string):
    return string[:len(string) - 1]


def create_rule(key, val, selector):
    return {
        "selector": selector,
        "rules": [
            {
                "name": key,
                "value": val
            }
        ]
    }
