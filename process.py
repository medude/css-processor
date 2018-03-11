import args
import beautify
from tree.create import to_tree
from tree.directives import resolve_directives
from tree.export import to_css
from tree.variables import *

with open(args.get_source()) as source:
    data = beautify.strip_whitespace_file(source)
    process_tree = to_tree(data, args.get_source())
    process_tree = substitute_constants(process_tree)
    process_tree = change_vars(process_tree)
    process_tree = vars_to_rules(process_tree)

    process_tree = resolve_directives(process_tree)

    css = to_css(process_tree)
    css = beautify.minify_css(css)

    with open(args.get_dest(), "w") as dest:
        dest.write(css)
