def to_css(tree, shrink=True):
    line_ending = "" if shrink else "\n"
    tab = "" if shrink else "\t"
    space = "" if shrink else " "

    css = ""

    for directive in tree["directives"]:
        css += "@" + directive["name"] + " " + directive["value"] + ";" + line_ending
    css += line_ending

    for selector in tree["rules"]:
        css += selector["selector"] + space + "{" + line_ending
        for rule in selector["rules"]:
            css += tab + rule["name"] + ":" + space + rule["value"] + ";" + line_ending
        css += "}" + line_ending + line_ending

    return css
