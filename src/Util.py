def get_fixed_path(path, replace_backslash=False, add_backslash=False):
    if replace_backslash:
        path = path.replace("\\", "/")

    if add_backslash:
        if not path.endswith("/"):
            path += "/"
    return path
