def combine_rules(tree):
    tmp = []

    for selector in tree["rules"]:
        is_copy = False
        for tmp_selector in tmp:
            if selector["selector"] == tmp_selector["selector"]:
                tmp_selector["rules"] += selector["rules"]
                is_copy = True
                break
        if not is_copy:
            tmp.append(selector)

    tree["rules"] = tmp

    return tree
