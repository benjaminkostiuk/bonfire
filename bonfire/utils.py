import os

'''
Build an absolute path from a relative path in the bonfire package directory
'''
def build_abs_path(rel_path):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    abs_path = os.path.join(current_dir, rel_path)
    return abs_path