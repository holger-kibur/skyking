

def dict_mask(source, key_list):
    return {key: val for key, val in source.items() if key in key_list}