import args
from tree.create import to_tree
from tree.directives import resolve_directives
from tree.export import to_css
from tree.rules import combine_rules
from tree.variables import *


if __name__ == "__main__":
    with open(args.get_source()) as source:
        data = source.readlines()
        process_tree = to_tree(data, args.get_source())
        process_tree = resolve_directives(process_tree)
        process_tree = substitute_constants(process_tree)
        process_tree = change_vars(process_tree)
        process_tree = vars_to_rules(process_tree)
        process_tree = combine_rules(process_tree)

        css = to_css(process_tree , False)

        with open(args.get_dest(), "w") as dest:
            dest.write(css)
