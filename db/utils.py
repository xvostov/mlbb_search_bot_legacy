def get_attr_string(obj):
    obj_attrs_dict = obj.__dict__
    return [f"{key}={obj_attrs_dict.get(key)}" for key in obj_attrs_dict if key[0] != "_"]