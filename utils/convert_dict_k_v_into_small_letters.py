def convert_dict_k_v_small_letters(dictionary: dict):
    return {k.lower(): str(v).lower() for k, v in dictionary.items()}