def to_css(tree):
    selectors = {}

    for rule in tree["rules"]:
        if not rule["selector"] in selectors:  # Ensure there is a list
            selectors[rule["selector"]] = {}

        selectors[rule["selector"]][rule["name"]] = rule["value"]

    css = ""

    for directive in tree["directives"]:
        css += "@" + " ".join(directive) + ";\n"

    for selector, rules in selectors.items():
        css += selector + " {\n"
        for name, value in rules.items():
            css += "  " + name + ": " + value + ";\n"
        css += "}\n"

    return css
