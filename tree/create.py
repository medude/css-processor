import re

import sys

from States import States
from tree.variables import const_char, var_char


def to_tree(data, path="."):
    # Combine everything into one line
    tmp = ""
    for line in data:
        tmp += line
    one_css = tmp

    curr_state = States.INITIAL

    variables = []
    constants = []
    rules = []
    directives = []

    tmp_list = []

    for char in one_css:
        if curr_state is States.INITIAL:
            tmp = "" # Clear from last state

            # DIRECTIVE
            if char is "@":
                curr_state = States.DIRECTIVE
                tmp_list = [0, "", ""]

            # CONSTANT
            elif char is const_char:
                curr_state = States.CONSTANT
                tmp_list = [0, "", ""]

            # VARIABLE
            elif char is var_char:
                curr_state = States.VARIABLE
                tmp_list = [0, "", ""]

            # RULE
            elif re.match(r"[a-zA-Z#*.]", char):
                curr_state = States.RULE
                tmp_list = [0, char, "", "", []]

            else:
                pass  # Must be whitespace
        elif curr_state is States.DIRECTIVE:
            result = directive_char(char, tmp_list, curr_state, directives)
            tmp_list = result["tmp_list"]
            curr_state = result["curr_state"]
            directives = result["directives"]
        elif curr_state is States.CONSTANT:
            # How tmp_list is used:
            #   0: the state
            #       0: reading name, write chars to 1
            #       1: reading value, write chars to 2
            #   1: the constant's name (before the colon)
            #   2: the constant's value (after the colon)
            if tmp_list[0] is 0:
                if char is ":":  # Done reading name
                    tmp_list[0] = 1
                else:
                    tmp_list[1] += char
            elif tmp_list[0] is 1:
                if char is ";":  # End of constant
                    constants.append({
                        "name": tmp_list[1].strip(),
                        "value": tmp_list[2].strip()
                    })
                    curr_state = States.INITIAL
                else:
                    tmp_list[2] += char
            else:
                tmp += char
        elif curr_state is States.VARIABLE:
            # How tmp_list is used:
            #   0: the state
            #       0: reading name, write chars to 1
            #       1: reading value, write chars to 2
            #   1: the constant's name (before the colon)
            #   2: the constant's value (after the colon)
            if tmp_list[0] is 0:
                if char is ":":  # Done reading name
                    tmp_list[0] = 1
                else:
                    tmp_list[1] += char
            elif tmp_list[0] is 1:
                if char is ";":  # End of variable
                    variables.append({
                        "name": tmp_list[1].strip(),
                        "value": tmp_list[2].strip()
                    })
                    curr_state = States.INITIAL
                else:
                    tmp_list[2] += char
            else:
                tmp += char
        elif curr_state is States.RULE:
            # How tmp_list is used:
            #   0: state
            #       0: reading selector, write chars to 1
            #       1: reading rule name, write chars to 2
            #       2: reading rule value, write chars to 3
            #       3: waiting for next rule name, or end of rule block
            #   1: selector
            #   2: current rule name
            #   3: current rule value
            #   4: list of rules objects already read
            #       name: name of the rule
            #       value: value of the rule

            # Reading Selector #
            if tmp_list[0] is 0:
                if char is "{":  # End of selector
                    tmp_list[1] = tmp_list[1].strip()
                    if not re.match(r"^[-_.#*A-Za-z0-9>()[\]:+~=| ]+$", tmp_list[1]):
                        print("ERROR: invalid selector: " + tmp_list[1])
                        sys.exit(-1)
                    tmp_list[0] = 1
                else:
                    tmp_list[1] += char

            # Reading Rule Name #
            elif tmp_list[0] is 1:
                if char is ":":  # End of rule name
                    tmp_list[2] = tmp_list[2].strip()
                    if not re.match(r"-?[_a-zA-Z]+[_a-zA-Z0-9-]*", tmp_list[2]):
                        print("Invalid rule name: " + tmp_list[2])
                        sys.exit(-1)
                    tmp_list[0] = 2
                elif re.match(r"[_a-zA-Z0-9- ]", char):
                    tmp_list[2] += char
                elif re.match(r"\s", char):
                    pass  # Ignore misc whitespace like newlines or tabs
                else:
                    print("Invalid character in rule name: " + char)

            # Reading Rule Value #
            elif tmp_list[0] is 2:
                if char is ";":  # End of rule value
                    tmp_list[3] = tmp_list[3].strip()
                    tmp_list[4].append({
                        "name": tmp_list[2],
                        "value": tmp_list[3]
                    })
                    tmp_list[0] = 3
                else:
                    tmp_list[3] += char

            # Waiting for Next #
            elif tmp_list[0] is 3:
                if char is "}":  # End of the rules
                    rules.append({
                        "selector": tmp_list[1],
                        "rules": tmp_list[4]
                    })
                    curr_state = States.INITIAL
                elif re.match(r"[-_a-zA-Z]", char):
                    tmp_list[0] = 1
                    tmp_list[2] = char
                    tmp_list[3] = ""

    return {
        "vars": variables,
        "consts": constants,
        "rules": rules,
        "directives": directives,
        "path": path
    }


def directive_char(char, tmp_list, curr_state, directives):
    # How tmp_list is used:
    #   0: the state
    #       0: reading name, write chars to 1
    #       1: reading value, write chars to 2
    #   1: the directive's name (before the space)
    #   2: the directive's value (after the space)
    if tmp_list[0] is 0:
        if char is " ":  # Done reading name
            tmp_list[0] = 1
        else:
            tmp_list[1] += char
    elif tmp_list[0] is 1:
        if char is ";":  # End of directive
            directives.append({
                "name": tmp_list[1],
                "value": tmp_list[2]
            })
            curr_state = States.INITIAL
        else:
            tmp_list[2] += char
    return {
        "tmp_list": tmp_list,
        "curr_state": curr_state,
        "directives": directives
    }
