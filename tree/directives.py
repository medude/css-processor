import os

import beautify
from tree.create import to_tree


def resolve_directives(tree):
    directives = tree["directives"]
    tree["directives"] = []  # Empty now to append later

    for directive in directives:
        if directive["name"] == "import" and len(directive["value"].split(" ")) == 1:
            # It's an import with no media query
            starting_path = os.path.dirname(os.path.abspath(tree["path"]))
            full_path = os.path.join(starting_path, directive["value"][1:-1])  # Strip quotes and join paths

            with open(full_path) as imported_file:
                data = beautify.strip_whitespace_file(imported_file)
                new_tree = to_tree(data, full_path)

                tree["rules"] = new_tree["rules"] + tree["rules"]  # Merge the rules
        else:
            # Can't deal with directive, add it back
            tree["directives"].append(directive)

    return tree
