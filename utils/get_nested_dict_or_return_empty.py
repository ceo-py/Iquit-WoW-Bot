def get_nested_dict_or_return_empty(source_for_dic, key):
    try:
        return source_for_dic.get(key, [{}])[0]
    except IndexError:
        return {}
