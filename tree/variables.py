from tree.utils import *


def vars_to_rules(tree):
    rules = tree["rules"]
    variables = tree["vars"]

    for name, value in variables.items():
        new_val = "--" + name[1:]  # Change to CSS variable
        rules.append(create_rule(new_val, value["value"], value["scope"]))

    tree["rules"] = rules
    return tree


def change_vars(tree):
    rules = tree["rules"]

    tmp = []
    for rule in rules:
        if is_var(rule["value"]):
            new_val = "var(--" + rule["value"][1:] + ")"  # Change to CSS variable
            rule["value"] = new_val
        tmp.append(rule)

    tree["rules"] = tmp
    return tree


def substitute_constants(tree):
    rules = tree["rules"]
    consts = tree["consts"]

    tmp = []
    for rule in rules:
        if is_const(rule["value"]):
            rule["value"] = consts[rule["value"]]
        tmp.append(rule)

    tree["rules"] = tmp
    return tree
