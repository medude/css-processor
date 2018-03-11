from tree.utils import *


def to_tree(data, path="."):
    variables = {}
    constants = {}
    rules = []
    directives = []

    curr_selector = ""

    for line in data:
        if ends_with(line, "{"):
            # Must be a selector
            # This means that the opening brace must be on the same line as the selector
            curr_selector = strip_last_char(line).strip()  # Remove brace and whitespace
        elif ends_with(line, "}"):
            # End of selector
            curr_selector = ""
        elif ends_with(line, ";"):
            # Must be a rule, variable, or directive
            # Remove semicolon and look for vars, rules
            line = strip_last_char(line)
            if is_key_val(line):
                key_val = split_key_val(line)
                key = key_val["key"]
                val = key_val["val"]

                if is_var(key):
                    scope = curr_selector
                    if scope is "":
                        scope = ":root"
                    variables[key] = {
                        "value": val,
                        "scope": scope
                    }
                elif is_const(key):
                    constants[key] = val
                elif curr_selector is not "":  # Ensure is not a rule with no selector
                    rules.append(create_rule(key, val, curr_selector))
                else:
                    print("Cannot interpret line: \"" + line + "\"")
            elif line[:1] is "@":
                # It's a directive
                directive = line[1:].split(" ")
                directives.append(directive)

    return {
        "vars": variables,
        "consts": constants,
        "rules": rules,
        "directives": directives,
        "path": path
    }
