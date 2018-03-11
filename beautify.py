# This file contains beautification and anti-beautification
def strip_whitespace_file(file):
    data = file.readlines()
    tmp = []
    for line in data:
        line = line.strip()
        if line != '':
            tmp.append(line)
    return tmp


def minify_css(css):
    return "".join(css.split())
