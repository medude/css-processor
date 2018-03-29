import re

from tree.utils import *

var_char = "$"
const_char = "_"

valid_name_re = re.compile(r"(-|--)?[_a-zA-Z][_a-zA-Z0-9-]*")


def is_valid_name(name):
    return valid_name_re.match(name)


def is_var(key):
    return key[:1] == var_char and is_valid_name(key)


def is_const(key):
    return key[:1] == const_char and is_valid_name(key)


def vars_to_rules(tree):
    rules = tree["rules"]
    variables = tree["vars"]

    for var in variables:
        new_val = "--" + var["name"]  # Change to CSS variable
        rules.append(create_rule(new_val, var["value"], ":root"))

    tree["rules"] = rules
    return tree


def change_vars(tree):
    rules = tree["rules"]

    for selector in rules:
        for rule in selector["rules"]:
            if is_var(rule["value"]):
                new_val = "var(--" + rule["value"][1:] + ")"  # Change to CSS variable
                rule["value"] = new_val

    return tree


def substitute_constants(tree):
    rules = tree["rules"]
    consts = tree["consts"]

    for selector in rules:
        for rule in selector["rules"]:
            if is_const(rule["value"]):
                for const in consts:
                    if const["name"] == rule["value"][1:]:
                        rule["value"] = const["value"]
                        break

    return tree
