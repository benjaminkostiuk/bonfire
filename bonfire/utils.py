import os
import re

# Build an absolute path from a relative path in the bonfire package directory
def build_abs_path(rel_path):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    abs_path = os.path.join(current_dir, rel_path)
    return abs_path

# Remove the .exe at the end of a process name and capitalize
def format_process_name(process_name):
    exp = re.compile('^(.*)\.exe$')
    if exp.match(process_name):
        process_name = exp.match(process_name).group(1)
    return process_name.capitalize()