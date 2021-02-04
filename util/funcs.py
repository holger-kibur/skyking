

def dict_mask(source, key_list):
    return {key: val for key, val in source.items() if key in key_list}

def get_all_subclasses(cls):
    subs = set()
    for subclass in cls.__subclasses__():
        subs.update(get_all_subclasses(subclass))
    return subs