def remove_none_values(args: dict) -> dict:
    keys_to_be_removed = []
    for key in args:
        if args[key] is None:
            keys_to_be_removed.append(key)
    for key in keys_to_be_removed:
        del args[key]
    return args
